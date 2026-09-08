# Meine Fehler in diesem Archify-Versuch

09.09.2026 · Codex · Status: PARKED auf Samuels Anweisung

## Was Samuel wollte

Ein Projekt an kostenlose Modelle geben, deren verfügbare Ergebnisse an einen guten
Aggregator weiterreichen und eine verständliche visuelle Projektkarte erhalten.
Ausfälle einzelner Modelle sollten ein brauchbares Ergebnis nicht verhindern.
Der Aggregator sollte die Darstellung bauen. Samuel wollte das bestehende Archify anwenden.

## Was ich stattdessen gemacht habe

Ich habe zuerst ein eigenes Verfahren mit Snapshots, starren Chunks, vorgeschriebenem
Claim-JSON, exakter Zitat-/Zeilenprüfung, Merge, fünf Sichten, Bindings und mehreren
Prüfschritten aufgebaut. Die Infrastruktur wurde zum eigentlichen Arbeitsgegenstand.
Den funktionierenden Mimo-/Archify-Weg habe ich nicht zuerst reproduziert.

Der HAI-MCP-Teillauf lieferte nur vier akzeptierte Findings aus zwei von 21 Chunks.
Kein Scout wurde vollständig fertig. Der Composer wurde zwar erreicht, aber seine
Ausgabe scheiterte nach einer Bindingskorrektur an der Layoutprüfung. Samuel bekam
einen Fehlerbericht statt der gewünschten Karte. Die von ihm genannten 17 Minuten
waren dafür verschwendete Aufmerksamkeit, unabhängig von einzelnen gemessenen Laufzeiten.

Die vereinfachte Variante lieferte fünf inhaltliche Scout-Berichte und eine unbrauchbare
Tool-Ankündigung. Der Composer konnte daraus eine gehaltvollere Erklärung erstellen.
Ich hatte ihn aber ausdrücklich zu Markdown und ASCII aufgefordert. Die HTML zeigte
folglich Text. Eine nachträgliche SVG-Ausgabe blieb ebenfalls überwiegend ein langer
Bericht; die wesentlichen Erkenntnisse standen unter dem Schaubild.

Als Samuel das beanstandete, begann ich selbst einen Graphviz-Renderer zu schreiben.
Er musste mich erneut daran erinnern, dass der Aggregator diese Arbeit machen soll.
Ich nahm die Änderung zurück. Der spätere Archify-Reparaturversuch wurde von Samuel
beendet; er ist keine abgeschlossene Lieferung.

## Meine konkreten Fehlentscheidungen

1. **Ich habe das falsche Erfolgskriterium optimiert.**
   Eine Pipeline, die trotz Ausfällen bis zum Composer kommt, erfüllt nicht den Auftrag,
   ein brauchbares Ergebnis zu liefern. Grün laufende Tests ersetzen diese Beobachtung nicht.

2. **Ich habe unnötige Hürden eingeführt.**
   Exakte Zitat- und Zeilennummerngleichheit verwarf auch passende Textstellen mit falschen
   Zeilenangaben. Pflichtschemata und Reparaturbudgets machten das Ergebnis empfindlicher.
   Diese Kosten habe ich vor dem großen Lauf nicht gegen einen funktionierenden einfachen
   Referenzweg geprüft.

3. **Ich habe aus schwacher Durchführung zu viel über Modelle abgeleitet.**
   Timeouts, ungültiges JSON und fehlende Bestätigungen entstanden unter meinen Bedingungen.
   Sie belegen keine allgemeine Schwäche der Free-Modelle. Die früheren brauchbaren Mimo-
   Ergebnisse waren ein konkreter Gegenbeleg gegen meine implizite Erklärung.

4. **Ich habe bei der Vereinfachung das Produktziel verloren.**
   Weniger Pipeline-Code war sinnvoll. Archify durch einen Textbericht zu ersetzen war es
   nicht. Einfacher hätte heißen müssen: den vorhandenen Renderer und dessen Interaktionen
   nutzen, weniger eigene Infrastruktur dazwischen setzen.

5. **Ich habe Visualisierung mit Illustration verwechselt.**
   Ein Komponentenbild über einem Aufsatz macht die Informationen nicht visuell verständlich.
   Vertragswechsel, ungültige Leases, Drift, Nachweise und Kontrollgrenzen müssen durch
   Beziehungen, Zustände und fokussierte Ansichten erkennbar werden. Mehr Text im Kasten
   löst dieses Problem ebenfalls nicht.

6. **Ich habe Samuels Rollenverteilung wiederholt übergangen.**
   Meine Aufgabe war Orchestrierung und ein präziser Auftrag. Trotzdem begann ich selbst,
   die Darstellung zu implementieren. Das war eine falsche Entscheidung von mir und kein
   fehlender Kontext des Nutzers.

7. **Ich habe den besseren vorhandenen Ansatz zu spät ernst genommen.**
   archify-swarm lässt schon die Scouts auf eine Karte hinarbeiten, nutzt Quellen an den
   Elementen und komponiert nach architektonischer Bedeutung. Seine geführten Ansichten
   tragen eine Erzählung. Ich hätte diesen konkreten Weg zuerst lesen und übernehmen sollen.
   Auch dessen Merge beweist nur Codefundstellen, nicht automatisch die Bedeutung eines Claims;
   das rechtfertigt aber nicht mein eigenes übergroßes Ersatzverfahren.

8. **Ich habe den Aggregator mit einem unvollständigen Ausführungsvertrag gestartet.**
   Beim Reparaturversuch fehlte die aufruflokale Freigabe zum Lesen des benachbarten Repos.
   OpenCode lehnte Zugriffe automatisch ab. Das verursachte einen weiteren unterbrochenen
   Durchgang. Ich hätte den benötigten Zugriff beim Start sauber übergeben müssen.

9. **Ich habe Aktivität zu häufig als Fortschritt kommuniziert.**
   Mehrere Updates beschrieben laufende Modelle, Entwürfe und Checks, während Samuel weiter
   auf die eine brauchbare Karte wartete. Meine Kommunikation hätte früher und klarer sagen
   müssen: Das angeforderte Ergebnis fehlt weiterhin.

## Was die vorliegenden Ergebnisse tatsächlich belegen

- Die 18 vorhandenen Tests bestehen auch nach dem Verschieben. Sie prüfen Teilfunktionen,
  simulierte Modellantworten und alte Integrationspfade. Sie beweisen keine gute Visualisierung.
- Der vereinfachte Live-Lauf zeigt, dass mehrere Free-Modelle brauchbare Berichte liefern und
  ein starker Composer Widersprüche darin einordnen kann. Das ist ein brauchbarer Teilbefund.
- Die visuelle Zielqualität wurde nicht erreicht. Samuel hat sie ausdrücklich zurückgewiesen.
- Es gibt keinen hier abgeschlossenen, belastbaren A/B-Nachweis für die Überlegenheit meiner
  Pipeline. Auch die Nutzung einer Opus-Karte als Reparaturvorlage wäre kein unabhängiger Vergleich.
- Die Laufbelege bleiben lokal unter `.archify-project/`. Der Code-Commit archiviert einen
  fehlgeschlagenen Versuch; er erklärt ihn nicht nachträglich zu einem fertigen Produkt.

## Was ich daraus ableite

Zuerst den bereits erfolgreichen Weg reproduzieren. Den Auftrag am gewünschten Artefakt
formulieren. Die vorhandenen Werkzeuge nutzen. Den Aggregator die Komposition tatsächlich
machen lassen. Nach dem ersten sichtbaren Ergebnis beurteilen, ob die Informationen im Bild
ankommen, bevor weitere Infrastruktur entsteht.

Das sind Konsequenzen für meine Arbeit, kein neuer Bauplan und keine Fortsetzungsfreigabe.
Dieser Versuch bleibt geparkt. Es wird nichts weiter gestartet oder verbessert, bis Samuel
es ausdrücklich beauftragt.
