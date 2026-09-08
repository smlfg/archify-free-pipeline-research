# Dein Projektleser

```text
Projekt → sechs Free-Modell-Berichte → ein schlauer Composer → Erklärung + ASCII-Karte
```

Start: `bin/archify-project analyze /pfad/zum/projekt --learning samuel`

Jedes Free-Modell erhält einmal denselben Quelltext inklusive Tests und Dokumentation.
Die vorhandene Dateiauswahl schließt Secrets, Agent-Kontext und Build-Verzeichnisse aus;
Lockdateien und SVGs werden zusätzlich ausgelassen und in `input.json` aufgeführt.
Es gibt keine automatische Aufteilung über mehrere Kontextfenster: Sehr große Projekte
können das Kontextlimit eines Modells überschreiten. Das wird als Modellausfall erhalten.

Die Modelle liefern freie Textberichte. Alles Verfügbare geht zum Composer, auch Text aus
unvollständigen Läufen, mit dessen Status. Keine Chunk-Bestätigungen, kein Claim-JSON,
kein deterministischer Merge, keine Archify-Layoutprüfung. Der Composer ordnet und erklärt;
Quellenangaben sind dabei modellbasiert, nicht unabhängig verifiziert.

`index.html` zeigt den Textbericht direkt im Browser. `report.md` enthält denselben Text.
`scouts.md` und die einzelnen Modell-Traces bleiben erhalten. Fällt der Composer aus,
zeigt der Bericht die Scout-Texte. Liefert kein Scout Text, steht dort der Fehlschlag.
Exit 0 bedeutet Composer-Bericht geliefert, nicht vollständige Projektabdeckung.
Exit 2 bedeutet Rohberichte oder Fehlschlag; `summary.json` unterscheidet beides.

`--ref` wählt einen Git-Commit, `--snapshot-only` zeigt die Eingabe ohne Modellaufrufe.
`--scout-timeout` begrenzt jeden parallelen Leser (Standard 300 Sekunden).
Der Composer nutzt `openai/gpt-6-astra`, medium. Keine globale Installation oder Config-Änderung.

Der frühere Vergleichs-/Claim-/Diagramm-Pfad liegt noch als Altcode im Ordner, wird aber
vom Kommando nicht mehr aufgerufen. Die separate Schwesterarbeit unter
`archify/integrations/free-pipeline` wurde nicht verändert.
