"""Bounded OpenCode invocations; raw events survive every failure."""
from __future__ import annotations

import json
import os
import signal
import subprocess
import time
import threading
from pathlib import Path

from .evidence import digest, write_json

MODELS = ["opencode/" + name for name in (
    "mimo-v2.5-free", "ling-3.0-flash-fin-free", "nemotron-3-ultra-free",
    "nemotron-3.5-lightning-free", "muse-spark-1.3-contributor-free", "big-pickle")]
COMPOSER = "openai/gpt-6-astra"


def parse_events(raw, text_mode=False):
    parts, events, errors, usage = [], [], [], []
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        events.append(event)
        if event.get("type") == "error":
            errors.append(event)
        part = event.get("part", {})
        if event.get("type") == "text" and isinstance(part, dict):
            parts.append(part.get("text", ""))
        if event.get("type") == "tool_use":
            errors.append({"reason": "unexpected tool invocation", "event": event})
        if isinstance(part, dict) and ("tokens" in part or "cost" in part):
            usage.append({k: part[k] for k in ("tokens", "cost", "reason") if k in part})
    text = "\n".join(parts).strip()
    if text_mode:
        return {"answer": text or None, "errors": errors, "usage": usage, "events": len(events)}
    if text.startswith("```") and text.endswith("```"):
        text = "\n".join(text.splitlines()[1:-1])
    try:
        answer = json.loads(text)
        if not isinstance(answer, dict):
            raise ValueError("expected an object")
    except ValueError as exc:
        answer = None
        errors.append({"reason": "invalid JSON answer", "detail": str(exc)})
    return {"answer": answer, "errors": errors, "usage": usage, "events": len(events)}


class OpenCode:
    def __init__(self, executable="opencode"):
        self.executable = executable
        self.cancelled = threading.Event()
        self.lock = threading.Lock()
        self.processes = set()

    def cancel(self, *_):
        self.cancelled.set()
        with self.lock:
            for process in self.processes:
                if process.poll() is None:
                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass

    def version(self):
        return subprocess.check_output([self.executable, "--version"], text=True, timeout=15).strip()

    def call(self, model, prompt, out: Path, timeout, variant=None, text_mode=False):
        out.mkdir(parents=True, exist_ok=False)
        prompt_path = out / "prompt.txt"
        prompt_path.write_text(prompt, encoding="utf-8")
        if self.cancelled.is_set():
            receipt = {"status": "cancelled", "model": model, "answer": None}
            write_json(out / "receipt.json", receipt)
            return receipt
        env = os.environ.copy()
        env["PWD"] = str(out.resolve())
        # Invocation-local restrictions, never changes installed agent config.
        denied = {k: "deny" for k in ("*", "read", "edit", "glob", "grep", "bash", "task",
                  "skill", "lsp", "question", "webfetch", "websearch", "external_directory")}
        env["OPENCODE_CONFIG_CONTENT"] = json.dumps({
            "permission": denied, "share": "disabled",
            "agent": {"plan": {"permission": denied}}})
        env["OPENCODE_DISABLE_AUTOUPDATE"] = "true"
        env["OPENCODE_DISABLE_CLAUDE_CODE"] = "true"
        env["OPENCODE_DISABLE_EXTERNAL_SKILLS"] = "true"
        command = [self.executable, "run", "--pure", "--agent", "plan", "--model", model,
                   "--format", "json"]
        if variant:
            command.extend(["--variant", variant])
        start = time.monotonic()
        status, code = "invalid", None
        # stdin avoids both shell argument limits and attachment preview truncation.
        with prompt_path.open("r") as stdin, (out / "trace.jsonl").open("w") as stdout, (out / "stderr.txt").open("w") as stderr:
            try:
                process = subprocess.Popen(command, cwd=out, env=env, stdin=stdin, stdout=stdout, stderr=stderr, start_new_session=True)
                with self.lock:
                    self.processes.add(process)
                    if self.cancelled.is_set():
                        os.killpg(process.pid, signal.SIGTERM)
                try:
                    code = process.wait(timeout=max(1, timeout))
                except (subprocess.TimeoutExpired, KeyboardInterrupt):
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
                    status = "timeout"
                finally:
                    with self.lock:
                        self.processes.discard(process)
            except OSError as exc:
                stderr.write(str(exc))
        parsed = parse_events((out / "trace.jsonl").read_text(), text_mode=text_mode)
        if code == 0 and parsed["answer"] is not None and not parsed["errors"]:
            status = "complete"
        receipt = {"status": status, "exit_code": code, "model": model, "variant": variant,
                   "seconds": round(time.monotonic() - start, 3), "prompt_sha256": digest(prompt.encode()), **parsed}
        write_json(out / "receipt.json", receipt)
        return receipt
