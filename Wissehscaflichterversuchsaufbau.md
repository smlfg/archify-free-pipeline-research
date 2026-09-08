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

## Eigentliche Forschungsfrage

Wie beeinflusst die Aufgabenverteilung zwischen günstigen Modellen und einem starken Aggregator die Qualität einer verständlichen, codegestützten Architekturkarte?

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

Wir haben aus fehlgeschlagenen Versuchen einen neuen Skill-/Pipeline-Ansatz abgeleitet und eingebunden. Dass dessen Phasenaufteilung bessere Ergebnisse liefert, ist noch nicht gezeigt. Der laufende Versuch ist daher der Schritt von plausibler Hypothese zu Evidenz.

Der wissenschaftlich interessante Teil ist nicht die Menge des gebauten Codes, sondern die präzise Frage, die dokumentierten Fehlerbilder und der kontrollierte Vergleich zwischen Redundanz und Spezialisierung.

## Kurzfazit

Ja: wissenschaftlich wertvoll als explorativer Versuchsaufbau.

Noch nein: kein belastbarer Wirksamkeitsnachweis.

Der nächste belastbare Befund entsteht erst, wenn der laufende Vergleich mit gesicherten Prompts, Modellrollen, Rohantworten, Artefakten und Bewertungskriterien ausgewertet wird.
