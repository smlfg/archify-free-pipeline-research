"""Freeze source bytes and validate references without interpreting claims."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath

VIEWS = ("architecture", "workflow", "sequence", "dataflow", "lifecycle")
EXCLUDED = {".git", ".hermes", ".claude", ".codex", ".agents", ".opencode",
            "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache",
            "dist", "build", "target", ".next", "generated", ".archify-project"}
SECRET_NAME = re.compile(r"(^\.env($|\.)|credentials|secrets?|auth\.json|id_(rsa|ed25519)|\.(pem|key|p12)$)", re.I)
SECRET_TEXT = re.compile(r"-----BEGIN .*PRIVATE KEY-----|\b(?:sk-[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{30,})")


def digest(value):
    raw = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(project, *args):
    return subprocess.run(["git", "-C", str(project), *args], capture_output=True, check=True).stdout


def snapshot(project: Path, ref: str | None = None, exclude: Path | None = None):
    project = project.resolve(strict=True)
    if not project.is_dir():
        raise ValueError("Project must be a directory")
    files, excluded = {}, []
    try:
        revision = git(project, "rev-parse", "--verify", "--end-of-options", (ref or "HEAD") + "^{commit}").decode().strip()
    except subprocess.CalledProcessError:
        if ref:
            raise ValueError("--ref requires a valid Git commit") from None
        revision = None
    entries = []
    if ref:
        prefix = git(project, "rev-parse", "--show-prefix").decode().strip()
        for entry in git(project, "ls-tree", "-rz", "--full-tree", revision).split(b"\0"):
            if entry:
                header, name = entry.split(b"\t", 1)
                mode, kind, oid = header.decode().split()
                decoded = os.fsdecode(name)
                if not decoded.startswith(prefix):
                    continue
                entries.append((decoded[len(prefix):], mode, oid if kind == "blob" else None))
    else:
        try:
            names = git(project, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0")
            entries = [(os.fsdecode(n), None, None) for n in sorted(set(names)) if n]
        except subprocess.CalledProcessError:
            for root, dirs, names in os.walk(project, followlinks=False):
                for d in list(dirs):
                    p = Path(root) / d
                    if d in EXCLUDED or p.is_symlink():
                        excluded.append({"path": str(p.relative_to(project)), "reason": "excluded directory or symlink"})
                        dirs.remove(d)
                entries.extend((str((Path(root) / n).relative_to(project)), None, None) for n in names)
    for name, mode, oid in sorted(entries):
        relative = PurePosixPath(name)
        reason = None
        if relative.is_absolute() or ".." in relative.parts:
            reason = "unsafe path"
        elif any(p in EXCLUDED for p in relative.parts) or SECRET_NAME.search(relative.name):
            reason = "excluded path"
        elif mode in ("120000", "160000"):
            reason = "symlink or submodule"
        elif not ref and exclude is not None and (project / name).resolve().is_relative_to(exclude.resolve()):
            reason = "output directory"
        if reason:
            excluded.append({"path": name, "reason": reason})
            continue
        try:
            if ref:
                raw = git(project, "cat-file", "blob", oid)
            else:
                p = project / name
                if p.is_symlink() or not p.resolve().is_relative_to(project):
                    raise ValueError("symlink")
                raw = p.read_bytes()
            if b"\0" in raw:
                raise ValueError("binary")
            text = raw.decode("utf-8")
            if SECRET_TEXT.search(text):
                raise ValueError("credential pattern")
            files[name] = {"sha256": digest(raw), "text": text}
        except (OSError, ValueError, subprocess.CalledProcessError) as exc:
            excluded.append({"path": name, "reason": str(exc) if isinstance(exc, ValueError) else type(exc).__name__})
    if not files:
        raise ValueError("No eligible UTF-8 source files")
    return {"id": digest({k: v["sha256"] for k, v in files.items()}), "project": str(project),
            "revision": revision, "source": "commit" if ref else "worktree", "files": files, "excluded": excluded}


def chunks(snap, limit=24000):
    """Every source line is included once; no silent truncation."""
    result, packet, size = [], [], 0
    for path, data in snap["files"].items():
        lines = data["text"].splitlines(keepends=True)
        start, part = 1, []
        for number, line in enumerate(lines, 1):
            if size + len(line.encode()) > limit and (packet or part):
                if part:
                    packet.append({"path": path, "start": start, "end": number - 1, "text": "".join(part)})
                result.append({"id": digest(packet), "sections": packet})
                packet, part, size, start = [], [], 0, number
            part.append(line)
            size += len(line.encode())
        if part:
            packet.append({"path": path, "start": start, "end": len(lines), "text": "".join(part)})
        elif not lines:
            packet.append({"path": path, "start": 1, "end": 0, "text": ""})
    if packet:
        result.append({"id": digest(packet), "sections": packet})
    return result


def quote(snap, path, start, end):
    if path not in snap["files"] or type(start) is not int or type(end) is not int:
        raise ValueError("invalid path or line types")
    lines = snap["files"][path]["text"].splitlines()
    if not 1 <= start <= end <= len(lines):
        raise ValueError("line range outside snapshot")
    return "\n".join(lines[start - 1:end])


def merge(snap, scouts):
    accepted, rejected = {}, []
    for scout in scouts:
        for position, claim in enumerate(scout.get("claims", [])):
            try:
                if not isinstance(claim, dict):
                    raise ValueError("claim must be an object")
                statement, view = claim.get("statement"), claim.get("view")
                if not isinstance(statement, str) or not statement.strip() or view not in VIEWS:
                    raise ValueError("statement or view missing")
                refs = claim.get("references")
                if not isinstance(refs, list) or not refs or len(refs) > 3:
                    raise ValueError("references missing")
                validated = []
                for ref in refs:
                    if not isinstance(ref, dict):
                        raise ValueError("reference must be an object")
                    if type(ref.get("start")) is not int or type(ref.get("end")) is not int or ref["end"] - ref["start"] >= 100:
                        raise ValueError("reference must span at most 100 lines")
                    actual = quote(snap, ref["path"], ref["start"], ref["end"])
                    if actual != ref.get("quote"):
                        raise ValueError("quote mismatch")
                    validated.append({"path": ref["path"], "start": ref["start"], "end": ref["end"], "quote": actual})
                validated.sort(key=lambda r: (r["path"], r["start"], r["end"]))
                relationship = claim.get("relationship")
                if relationship is not None and (not isinstance(relationship, dict) or
                        not all(isinstance(relationship.get(k), str) and relationship[k] for k in ("from", "to", "label"))):
                    raise ValueError("invalid relationship")
                clean = {"statement": statement.strip(), "view": view, "references": validated,
                         "relationship": relationship}
                cid = "c-" + digest({"snapshot": snap["id"], **clean})[:20]
                if cid not in accepted:
                    accepted[cid] = {"id": cid, **clean, "found_by": [], "interpretation": "unreviewed"}
                if scout["model"] not in accepted[cid]["found_by"]:
                    accepted[cid]["found_by"].append(scout["model"])
            except (ValueError, KeyError, TypeError) as exc:
                rejected.append({"model": scout["model"], "position": position, "reason": str(exc), "claim": claim})
    claims = sorted(accepted.values(), key=lambda c: c["id"])
    for c in claims:
        c["found_by"].sort()
    groups = {}
    for claim in claims:
        for ref in claim["references"]:
            key = (ref["path"], ref["start"], ref["end"])
            group = groups.setdefault(key, {"path": ref["path"], "start": ref["start"], "end": ref["end"], "claims": [], "found_by": set()})
            group["claims"].append(claim["id"])
            group["found_by"].update(claim["found_by"])
    source_groups = [{**g, "found_by": sorted(g["found_by"])} for _, g in sorted(groups.items())]
    return {"snapshot": snap["id"], "claims": claims, "source_groups": source_groups, "rejected": rejected,
            "note": "References verified; statements are model interpretations, not deterministic semantic proof."}
