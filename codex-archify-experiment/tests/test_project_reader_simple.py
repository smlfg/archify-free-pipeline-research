"""Failure behavior of the simple route, with explicitly simulated models."""
import json
import threading
from argparse import Namespace

import pytest

from project_reader.runner import COMPOSER, MODELS, parse_events
from project_reader.simple import run


@pytest.mark.parametrize('composer_ok', [True, False])
def test_one_plain_report_survives_five_failures(tmp_path, composer_ok):
    project = tmp_path / 'project'
    project.mkdir()
    (project / 'main.py').write_text('print("hello")\n')
    class Runner:
        cancelled = threading.Event()
        def call(self, model, prompt, out, timeout, **kwargs):
            if model == COMPOSER:
                assert 'main.py:1' in prompt
                return {'status': 'complete' if composer_ok else 'timeout',
                        'answer': 'App -> stdout\nmain.py:1' if composer_ok else None}
            return {'status': 'complete' if model == MODELS[0] else 'timeout',
                    'answer': 'App prints hello (main.py:1). <script>bad</script>' if model == MODELS[0] else None}
    out = tmp_path / 'out'
    options = Namespace(output=out, project=project, ref=None, snapshot_only=False,
                        scout_timeout=1, composer_timeout=1, learning='samuel')
    assert run(options, Runner()) == (0 if composer_ok else 2)
    assert (out / 'report.md').read_text()
    assert '<script>bad</script>' not in (out / 'index.html').read_text()
    summary = json.loads((out / 'summary.json').read_text())
    assert summary['reports'] == 1
    assert summary['status'] == ('composed' if composer_ok else 'scout_reports_only')


def test_plain_text_is_not_rejected_as_invalid_json():
    result = parse_events(json.dumps({'type': 'text', 'part': {'text': 'Useful report'}}), text_mode=True)
    assert result['answer'] == 'Useful report'
    assert result['errors'] == []
