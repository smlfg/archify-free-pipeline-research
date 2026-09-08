# Wissenschaftlicher Versuchsaufbau

Stand: 2026-09-09 00:43 CEST

## Einordnung

Die heutige Arbeit war überwiegend Harness-Engineering: Wir haben nicht einfach ein Diagramm gebaut, sondern ein Verfahren entworfen, in dem mehrere Modelle ein Repository lesen, ihre Ergebnisse erhalten bleiben und ein stärkerer Aggregator daraus eine verständliche Architekturkarte komponiert.

Gleichzeitig enthielt die Arbeit exploratives Coding und einen Ansatz zum Varianztest. Meine Umsetzung war zeitweise genau das unkontrollierte Bauen, das Samuel kritisiert hat: zu viel Infrastruktur, zu spät am sichtbaren Ergebnis geprüft, zu früh technische Teilerfolge als Fortschritt kommuniziert.

## Begriffe

| Begriff | Was davon passiert ist |
| --- | --- |
| Vibecoding | Es wurde zu viel Code erzeugt, ohne früh genug am sichtbaren Ergebnis zu prüfen, ob der Auftrag erfüllt ist. Samuel musste wiederholt korrigieren, dass eine technisch laufende Pipeline noch kein brauchbares Produkt ist. |
| Harness-Engineering | Aufgabenverteilung, Modellzugriff, Kontext, Übergaben, Ausfallverhalten und Ergebnisprüfung wurden gestaltet. Das ist der eigentliche Kern eines Harness. |
| Varianztest | Mehrere Modelle dasselbe Repo unabhängig lesen zu lassen, macht unterschiedliche Funde und Auslassungen sichtbar. Die früheren Vergleichsläufe passen zu dieser Forschungsfrage. |
| Arbeitsteilung | Die Variante „ein Modell pro Phase“ untersucht Spezialisierung. Sie ist kein sauberer Modellvergleich, weil jedes Modell eine andere Aufgabe bekommt. |

## Forschungsfrage

Does redundant full-repository scouting or specialized scouting produce better source-grounded architecture representations when composed by a stronger model?

Status: Exploratory. Ein neuer größerer Lauf ist ermutigend für den Fächer und unterstützt die Varianz-/Low-Overlap-Hypothese; eine vollständige Strategie ist weiterhin noch nicht als überlegen gezeigt.

Deutsch: Produziert redundantes Full-Repository-Scouting oder spezialisiertes Scouting bessere source-grounded Architektur-Repräsentationen, wenn ein stärkeres Modell sie komponiert?

Darin stecken zwei unterscheidbare Hypothesen:

1. Redundanz-Hypothese
   Mehrere vollständige Analysen desselben Repos entdecken unterschiedliche wichtige Aspekte. Der Mehrwert entsteht aus Varianz und Überlappung.

2. Spezialisierungs-Hypothese
   Ein Modell pro Analysebereich erreicht bei gleichem Budget mehr Tiefe, riskiert aber Lücken, wenn ein Spezialist ausfällt oder seinen Bereich schlecht versteht.

## Was bisher wissenschaftlich wertvoll ist

Als explorative Untersuchung ist der Versuch wertvoll. Er liefert noch keinen belastbaren Nachweis, dass die neue Methode besser ist, aber er erzeugt prüfbare Hypothesen und konkrete Fehlerbilder.

Beobachtete Erkenntnisse:

- Strenge Ausgabeanforderungen können brauchbare Befunde aussortieren.
- Technisch grüne Prüfungen garantieren keine verständliche Darstellung.
- Modellkonsens ist keine Wahrheitsfunktion; seltene Einzelfunde können zentral sein.
- Der Merge-Schlüssel sollte die Codestelle sein, nicht das Modelllabel.
- Eine technisch laufende Pipeline ist noch kein verständliches Produkt.
- Fehlgeschlagene Läufe sind verwertbar, wenn Prompt, Modellzuordnung, Kosten, Rohantworten und Artefakte erhalten bleiben.

## Neuer Befund

Der neue größere Lauf ist ein ermutigender Befund für den Fächer-Ansatz. „Hypothese bestätigt“ wäre aber stärker, als diese Zahlen tragen:

```text
110 Belege aus 6 Karten -> 53 verifizierte Konzepte
```

| Konsensniveau | belegt | unbelegt |
| --- | ---: | ---: |
| >=3 Modelle | 12 | 0 |
| <=2 Modelle | 41 (77%) | 9 |

| Modell | Cluster |
| --- | ---: |
| muse-spark-1.3 | 22 |
| nemotron-3-ultra | 22 |
| ling-3.0-flash-fin | 18 |
| mimo-v2.5 | 17 |
| muse-spark-1.2 | 11 |
| nemotron-3.5-lightning | 0 |

Interpretation: 41 von 53 belegten Clustern kommen nur von ein oder zwei Modellen. Ein Filter „mindestens drei Modelle müssen zustimmen“ würde also rund 77% der gefundenen Cluster aussortieren. Unterschiedliche Perspektiven tragen viel zur gesammelten Abdeckung bei.

Kandidaten ohne fertiges HTML bleiben nutzbar, wenn ihre Quellen in den Merge eingehen. Genau das ist ein Ziel des Harness: Ein Modell muss den Darstellungsschritt nicht abschließen, damit seine Analyse dem Aggregator hilft.

Einschränkungen: „Größeres Projekt -> weniger Überlappung“ ist damit gestützt, noch nicht bestätigt. Zwischen zwei Projekten ändern sich auch Struktur und Aufgabeninhalt. Außerdem sind 77% der gefundenen Cluster nicht automatisch 77% der gesamten wichtigen Projektinformation.

Unstimmigkeit: „Beide Nemotrons brauchbar“ passt nicht ohne Erklärung zu `nemotron-3.5-lightning` mit 0 Clustern. Möglich ist: formal brauchbarer Kandidat, aber keine für den Merge verwertbaren Quellen. Das muss getrennt werden.

Begriffspräzision: In diesem Merge bedeutet „verifiziert“ zunächst, dass die referenzierte Codestelle existiert. Es beweist noch nicht automatisch, dass die behauptete architektonische Bedeutung vollständig stimmt.

Für die Frage „War die Mühe wert?“ ist das ein konkreter Teilerfolg: Der Fächer sammelt zusätzliche Befunde und überlebt unvollständige Ausgaben. Ob daraus der gewünschte Nutzen entsteht, entscheidet sich daran, ob der Composer diese Befunde in eine Karte übersetzt, mit der Samuel tatsächlich mehr versteht.

## Kontrollierter Vergleich

Für einen belastbaren Vergleich braucht es mindestens diesen Aufbau:

```text
Dasselbe Repo
Derselbe Commit
Dieselben Modelle
Dieselbe Zeit-/Kostenklasse
        │
        ├── A: sechs vollständige Repo-Analysen
        │
        └── B: sechs spezialisierte Analysebereiche
                │
        Gleicher Aggregator
        Gleicher Bildauftrag
                ↓
Korrektheit · wichtige Funde · Verständlichkeit
Zeit · Kosten · Ausfallverhalten
```

Mehrere Wiederholungen sind wichtig, damit ein zufällig guter Lauf nicht mit einem echten Effekt der Aufgabenverteilung verwechselt wird. Weitere Repos wären nötig, um über HAI-MCP oder einzelne Fallbeispiele hinaus Aussagen zu machen.

## Messkriterien

Ein Lauf sollte nicht nur nach „hat HTML erzeugt“ bewertet werden. Relevante Kriterien sind:

- Korrektheit der Codebezüge: Stimmen Pfade, Zeilen, Funktionen und Verantwortlichkeiten?
- Wichtige Funde: Werden zentrale Architekturpunkte erkannt, auch wenn nur wenige Modelle sie finden?
- Auslassungen: Welche wichtigen Komponenten fehlen?
- Verständlichkeit: Kann Samuel anhand der Karte das System top-down erklären?
- Aggregator-Verhalten: Wählt der Aggregator nach Bedeutung oder nur nach Häufigkeit?
- Robustheit: Was passiert bei Timeouts, ungültigem JSON, fehlenden Modellen oder unvollständigen Scouts?
- Kosten/Zeit: Wie teuer ist der Befund im Verhältnis zum Nutzen?
- Artefaktqualität: Liefert das Ergebnis eine echte visuelle Karte oder nur Text in einem HTML-Rahmen?

## Was gesichert werden muss

Für den laufenden Versuch müssen erhalten bleiben:

- exakter Repo-Pfad und Commit
- vollständiger Auftrag/Prompt
- Modellliste und Modellrollen
- alle Scout-Rohantworten, auch fehlerhafte
- Aggregator-Prompt und Aggregator-Antwort
- erzeugte Claims, Zwischenartefakte und finale Karte
- Zeit, Kosten, Token- oder Rate-Limit-Signale
- Validierungsberichte und visuelle Prüfung
- menschliche Bewertung: Was war verständlich, was nicht?

Ohne diese Spuren kann man hinterher nicht unterscheiden, ob die Aufgabenverteilung geholfen hat oder ob nur einzelne Modelle zufällig besser waren.

## Ehrlicher Stand

Wir haben aus fehlgeschlagenen Versuchen einen neuen Skill-/Pipeline-Ansatz abgeleitet und eingebunden. Der neue größere Lauf zeigt, dass Low-Consensus-Funde sehr viel Substanz tragen können. Dass eine vollständige Phasenaufteilung als Strategie besser ist, ist damit plausibler, aber noch nicht allgemein gezeigt. Der nächste Prüfpunkt ist die Composer-Qualität: mehr Befunde müssen in eine verständlichere Karte übersetzt werden, nicht nur in mehr Material.

Der wissenschaftlich interessante Teil ist nicht die Menge des gebauten Codes, sondern die präzise Frage, die dokumentierten Fehlerbilder und der kontrollierte Vergleich zwischen Redundanz und Spezialisierung.

## Kurzfazit

Ja: wissenschaftlich wertvoll als explorativer Versuchsaufbau.

Noch nein: kein allgemeiner Wirksamkeitsnachweis für eine überlegene Gesamtstrategie.

Der nächste belastbare Befund entsteht erst, wenn der laufende Vergleich mit gesicherten Prompts, Modellrollen, Rohantworten, Artefakten und Bewertungskriterien ausgewertet wird.
