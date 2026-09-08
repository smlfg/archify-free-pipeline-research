"""Offline transport fixtures exercise real snapshot/merge/Archify delivery.

FakeRunner is intentionally not model-quality or semantic evidence.
"""
import argparse
import copy
import json
import subprocess
from pathlib import Path

import pytest

from project_reader.composer import bundle_errors, element_keys
from project_reader.evidence import VIEWS, chunks, merge, quote, snapshot, write_json
from project_reader.pipeline import run
from project_reader.runner import MODELS, parse_events

ROOT = Path(__file__).resolve().parents[1]
ARCHIFY = ROOT / "archify/archify"


def sample(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    (project / "app.py").write_text('def authorize_session(owner):\n    return bool(owner)\n\n# NEXT_STEP history, not migration\n')
    return project


def claim(statement="authorize_session checks owner", quote_text="def authorize_session(owner):"):
    return {"statement": statement, "view": "architecture", "references": [
        {"path": "app.py", "start": 1, "end": 1, "quote": quote_text}]}


def test_snapshot_chunks_and_exclusions(tmp_path):
    project = sample(tmp_path)
    (project / ".env").write_text("PRIVATE=value")
    (project / "outside").symlink_to("/etc/passwd")
    (project / "binary").write_bytes(b"\0x")
    (project / "secret.txt").write_text("sk-" + "x" * 40)
    snap = snapshot(project)
    assert set(snap["files"]) == {"app.py"}
    assert len(snap["excluded"]) == 4
    packets = chunks(snap, limit=35)
    restored = "".join(s["text"] for p in packets for s in p["sections"])
    assert restored == snap["files"]["app.py"]["text"]
    assert len(packets) > 1
    assert all(quote(snap, s["path"], s["start"], s["end"]) == "\n".join(s["text"].splitlines()) for p in packets for s in p["sections"])


def test_commit_snapshot_excludes_dirty_changes(tmp_path):
    project = sample(tmp_path)
    subprocess.run(["git", "init", "-q", str(project)], check=True)
    subprocess.run(["git", "-C", str(project), "add", "app.py"], check=True)
    # Commit is exclusively an ephemeral test fixture, not Samuel's worktree.
    subprocess.run(["git", "-C", str(project), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"], check=True)
    original = snapshot(project, "HEAD")
    (project / "app.py").write_text("changed\n")
    assert snapshot(project, "HEAD")["id"] == original["id"]
    assert snapshot(project)["id"] != original["id"]


def test_merge_preserves_interpretations_and_exact_identifiers(tmp_path):
    snap = snapshot(sample(tmp_path))
    claims = [claim(), claim("This writes artifacts"), claim(quote_text="def artifact_write(owner):")]
    result = merge(snap, [{"model": "one", "claims": claims + [claim()]}, {"model": "two", "claims": [claim()]}])
    assert len(result["claims"]) == 2
    assert len(result["rejected"]) == 1
    assert {c["statement"] for c in result["claims"]} == {"authorize_session checks owner", "This writes artifacts"}
    first = next(c for c in result["claims"] if c["statement"].startswith("authorize"))
    assert first["found_by"] == ["one", "two"]
    assert first["interpretation"] == "unreviewed"
    assert first["references"][0]["quote"] == "def authorize_session(owner):"
    assert len(result["source_groups"]) == 1
    assert len(result["source_groups"][0]["claims"]) == 2
    assert merge(snap, [{"model": "two", "claims": [claim()]}, {"model": "one", "claims": claims}]) == result


@pytest.mark.parametrize("ref", [
    {"path": "../app.py", "start": 1, "end": 1},
    {"path": "app.py", "start": True, "end": 1},
    {"path": "app.py", "start": 1, "end": 99},
])
def test_bad_references(tmp_path, ref):
    snap = snapshot(sample(tmp_path))
    c = claim()
    c["references"] = [{**ref, "quote": "anything"}]
    assert not merge(snap, [{"model": "one", "claims": [c]}])["claims"]


def test_nonobject_reference_rejected(tmp_path):
    c = claim()
    c["references"] = [None]
    result = merge(snapshot(sample(tmp_path)), [{"model": "one", "claims": [c]}])
    assert not result["claims"] and result["rejected"]


def test_pinned_hai_review_is_actual_snapshot_evidence():
    fixture = json.loads((ROOT / "tests/fixtures/hai_mcp_review.json").read_text())
    # Portable fixture test protects exact names that were mistranslated in the old handoff.
    by_id = {c["id"]: c for c in fixture["checks"]}
    assert 'audit=self.append_audit' in by_id['audit-callback']['quote']
    assert 'mcp.run(transport="stdio")' in by_id['transport']['quote']
    assert 'history_dir' in by_id['history']['quote']


def test_event_errors_override_a_plausible_answer():
    raw = '\n'.join(json.dumps(e) for e in [{"type": "text", "part": {"text": '{"ready":true}'}}, {"type": "error", "error": "quota"}])
    parsed = parse_events(raw)
    assert parsed["answer"] == {"ready": True} and parsed["errors"]
    assert parse_events('{"type":"text","part":{"text":"not json"}}')["answer"] is None


EXAMPLES = dict(zip(VIEWS, ("web-app.architecture.json", "agent-tool-call.workflow.json", "cache-miss-request.sequence.json", "event-stream.dataflow.json", "agent-run.lifecycle.json")))


def fixture_bundle(cid, learning="samuel"):
    views = {}
    for view, name in EXAMPLES.items():
        candidate = json.loads((ARCHIFY / "examples" / name).read_text())
        candidate["meta"].pop("visual_preset", None)
        candidate["meta"].pop("output", None)
        views[view] = {"candidate": candidate, "bindings": {k: {"entity": "fixture", "claims": [cid]} for k in element_keys(candidate)}, "selection_reason": "Offline transport fixture, not a model finding"}
    return {"entities": [{"id": "fixture", "label": "Test fixture", "claims": [cid]}], "views": views,
            "learning": {"fixture": {"plain": "This is an offline integration fixture.", "glossary": [], "question": "Which argument enters authorize_session?", "hint": "Read the signature", "mastery": "Point to the argument"}} if learning == "samuel" else {}, "unresolved": ["Fixture: no model quality or semantic correctness measured"]}


def test_bindings_and_learning_required():
    merged = {"claims": [{"id": "c-fixture"}]}
    bundle = fixture_bundle("c-fixture")
    assert not bundle_errors(bundle, merged, "samuel")
    broken = copy.deepcopy(bundle)
    broken["views"]["architecture"]["bindings"].pop(next(iter(broken["views"]["architecture"]["bindings"])))
    assert bundle_errors(broken, merged, "samuel")
    broken = copy.deepcopy(bundle)
    broken["learning"]["fixture"].pop("question")
    assert bundle_errors(broken, merged, "samuel")


class FakeRunner:
    def __init__(self, snap, fail=None):
        self.snap, self.fail, self.prompts = snap, fail, []
    def version(self):
        return "TEST FIXTURE - NO REAL MODEL"
    def call(self, model, prompt, out, timeout, variant=None):
        out.mkdir(parents=True)
        self.prompts.append((model, prompt))
        if prompt.startswith('Return exactly'):
            answer = {"ready": True}
        elif prompt.startswith("Analyze"):
            data = json.loads(prompt.split('\n')[-1])
            answer = {"chunk_id": data["chunk_id"], "claims": [claim()]}
        else:
            cid = merge(self.snap, [{"model": MODELS[0], "claims": [claim()]}])["claims"][0]["id"]
            answer = fixture_bundle(cid)
        result = {"status": "invalid" if self.fail == model else "complete", "answer": answer, "seconds": 0, "usage": []}
        write_json(out / "receipt.json", result)
        return result


def args(project, out, command="analyze"):
    return argparse.Namespace(project=project, output=out, ref=None, archify=ARCHIFY, snapshot_only=False,
                              command=command, strategy="generalist", learning="samuel", scout_timeout=30, composer_timeout=120)


def test_failed_preflight_never_becomes_quality_score(tmp_path):
    project = sample(tmp_path)
    runner = FakeRunner(snapshot(project), fail=MODELS[1])
    out = tmp_path / "failed"
    assert run(args(project, out, "compare"), runner) == 2
    summary = json.loads((out / "summary.json").read_text())
    assert all(s["status"] == "invalid" for s in summary.values())
    assert len(runner.prompts) == 7
    assert (out / "index.html").exists()


def test_failed_first_arm_does_not_launch_second_arm(tmp_path):
    project = sample(tmp_path)
    class BadScout(FakeRunner):
        def call(self, model, prompt, out, timeout, variant=None):
            result = super().call(model, prompt, out, timeout, variant)
            if prompt.startswith('Analyze'):
                result['answer'] = {"claims": []}  # missing acknowledgement
            return result
    runner = BadScout(snapshot(project))
    out = tmp_path / 'stop-after-first'
    assert run(args(project, out, 'compare'), runner) == 2
    assert len(runner.prompts) == 7 + 6
    assert json.loads((out / 'specialist/summary.json').read_text())['complete_scouts'] == 0


def test_real_archify_delivery_with_fake_model_transport(tmp_path):
    project = sample(tmp_path)
    out = tmp_path / "delivered"
    runner = FakeRunner(snapshot(project))
    assert run(args(project, out), runner) == 0
    summary = json.loads((out / "generalist/summary.json").read_text())
    assert summary["complete_scouts"] == 6
    assert all(summary["delivered"].values())
    assert summary["semantic_review"] == "not_run"
    assert all((out / "generalist" / f"{v}.html").stat().st_size > 1000 for v in VIEWS)
    assert "authorize_session(owner)" in (out / "generalist/evidence.html").read_text()
    assert all("learning_mode" not in p for m, p in runner.prompts if m in MODELS)


@pytest.mark.parametrize("stage", ["preflight", "reading"])
def test_partial_policy_delivers_despite_one_failed_scout(tmp_path, stage):
    project = sample(tmp_path)
    class FailingScout(FakeRunner):
        def call(self, model, prompt, out, timeout, variant=None):
            result = super().call(model, prompt, out, timeout, variant)
            if model == MODELS[1] and ((stage == "preflight" and prompt.startswith("Return exactly")) or
                                      (stage == "reading" and prompt.startswith("Analyze"))):
                result["status"] = "invalid"
                result["answer"] = None
            return result
    runner = FailingScout(snapshot(project))
    out = tmp_path / 'partial'
    options = args(project, out)
    options.failure_policy = 'partial'
    assert run(options, runner) == 2  # usable partial output, NOT benchmark success
    summary = json.loads((out / 'generalist/summary.json').read_text())
    assert summary['complete_scouts'] == 5
    assert summary['composition_status'] == 'complete'
    assert summary['benchmark_eligible'] is False
    assert all(summary['delivered'].values())
    assert summary['browser_review'] == 'passed'
    assert 'partial' in summary['reason'].lower()
