---
name: archify-project
description: Read a project with free-model text reports and one strong composer, producing a plain project explanation and ASCII architecture map.
---

Run `<workspace>/bin/archify-project analyze <project> --learning samuel`.
The entrypoint is `../../bin/archify-project` relative to this skill directory.

Six free models receive the same eligible source packet, once each. Available text reports
feed one `openai/gpt-6-astra` composer call. No JSON claim schema or layout gate.
Failed scouts do not block composition. Failed composition leaves readable scout reports.

Open the output `index.html` directly, or read `report.md`. Inspect `summary.json` for
model failures. Sources are model-reported, not independently verified. Never call delivery
proof of complete code coverage, correct interpretation, or owner understanding.

`--ref <commit>` freezes committed source. `--snapshot-only` inspects the input without calls.
`--output <fresh-directory>` selects the output location. Secrets, excluded directories,
locks and SVGs are omitted; omissions are recorded. Large projects may exceed model context;
there is no automatic chunking. Preserve failures rather than reporting them as successful reads.

No global config changes, publication, or private biographical context required.
