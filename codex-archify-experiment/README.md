# Codex-Archify-Experiment

Status: PARKED. Auf Samuels Anweisung am 09.09.2026 aus dem Workspace-Hauptverzeichnis ausgelagert.
Dies ist der gesicherte Stand eines nicht zufriedenstellenden Experiments, keine freigegebene Lösung.

Enthält den von Codex verantworteten Projektleser, CLI, lokalen Skill und Tests.
Die eigenen Laufartefakte bleiben lokal unter `.archify-project/` erhalten und sind nicht Teil des Commits.
Sie enthalten eingefrorene Projektquellen und Modell-Traces; historische absolute Pfade wurden nicht umgeschrieben.
Der zuletzt gestartete Aggregator wurde vor dem Verschieben beendet. Sein Reparaturversuch ist unvollständig.

`archify` ist ein relativer Link auf das bestehende Nachbarprojekt `../archify`, keine Kopie und kein Bestandteil dieser Implementierung.
Die Integrationstests benötigen dieses Nachbarprojekt einschließlich seiner vorhandenen Laufzeitabhängigkeiten.

Lokaler Test aus diesem Ordner: `python3 -m pytest tests/test_project_reader.py tests/test_project_reader_simple.py -q`.
Die Tests belegen Teilfunktionen und simulierte Ausfallpfade; sie belegen keine brauchbare visuelle Projekterklärung.
