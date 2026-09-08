# Komponisten-Input: hai-mcp Architektur-Karte aus 37 verifizierten Befunden

**Quelle:** `hai-mcp.claims.md` (5 unabhängige Karten, deterministisch nach Codestelle gemergt, gegen HEAD verifiziert)

**Du bist Komponist, nicht Scout.** Deine Aufgabe: aus 37 belegten Konzepten EINE Architektur-Karte formen. Du wählst nach Bedeutung, nicht nach Häufigkeit. Du darfst keine neuen Belege erfinden — nur die 37 unten verwenden, plus gezieltes Nachlesen der genannten Codestellen (max. 5 Stellen).

## Deine Constraints (einklagbar)

1. **Bedeutung > Häufigkeit.** "5/5 gefunden" heißt nur: leicht zu sehen. Wenn du einen 1/5-Befund (z. B. Audit-Kette) für architektonisch wichtiger hältst als einen 5/5-Befund (z. B. Config), wähle ihn — und begründe es.
2. **Keine neuen Codestellen erfinden.** Wenn du eine Stelle brauchst, die nicht in den 37 steht, lies sie nach und melde sie explizit als "zusätzlich geöffnet" mit Pfad:Zeile.
3. **Maximal 12 Knoten** (Vergleichbarkeit mit den Einzelkarten). Wenn du weniger wählst, begründe warum.
4. **Jeder Knoten muss eine der 37 Stellen als Hauptbeleg haben.** Label frei wählbar, aber Codestelle verpflichtend.
5. **3 Guided Views** als zusammenhängende Erzählung, die das Wesen des Systems in 3 Schritten zeigt. Jede View referenziert konkrete Knoten.

## Die 37 belegten Cluster (gruppiert nach Konsens)

### 5/5 — leicht zu sehen (5 Konzepte)
- `mission.py:98` — MissionEngine
- `owner_gate.py:190` — OwnerGate
- `paths.py:47` — confined_artifact_dir (Path Confinement / Fail-closed / Project FS)
- `server.py:9` — FastMCP / Tool Surface
- `state.py:44` — ControlPlane

### 4/5 — fast vollständig (3 Konzepte)
- `owner_gate.py:354` — Owner-Gate Folgeaktion
- `server.py:429` — Tool-Handler / Server Wiring
- `storage.py:10` — JSONL Storage

### 3/5 — solide Mehrheit (7 Konzepte)
- `http_transport.py:10` + `:36` — HTTP Transport
- `locking.py:13` — Locking
- `owner_gate.py:119` + `:148` — Owner-Gate Regeln
- `paths.py:76` — Path-Erweiterung
- `projects.py:30` — Project Registry
- `config.py:12` + `:83` — Config (umstritten, siehe Contested-Box)

### 2/5 — Minderheit, aber belegt (6 Konzepte)
- `mission.py:121`, `:174`, `:912` — Mission State Machine Etappen
- `state.py:76` — State restore
- `docs/client-snippets/claude-code.mcp.json:1` — Client-Integration
- `pyproject.toml:15` — (Leerzeile, **kein Code** — siehe Hinweis)

### 1/5 — Einzelfunde, oft die wertvollsten (16 Konzepte)
- `__main__.py:1` — Entry Point
- `boundary.py:13` — strict_optional_time_limit_hours (boundary enforcement)
- `eval_impact.py:78` — **Eval-Harness**
- `ids.py:32` — validate_generated_id
- `mission.py:246` — Mission follow-up
- `mission.py:402` — Mission acceptance
- `mission.py:615` — Mission artifact write
- `mission.py:1360` — **Audit-Kette / _verify_evidence_path**
- `server.py:305` + `:450` — Tool-Handler Details
- `state.py:26` — HAI_HOME resolution
- `state.py:306` — State persistence
- `state.py:376` — State migration
- `storage.py:33` — Storage write

## Die Contested-Box (modell-abhängig)

Falls du Config (config.py:12, `:83`) als Knoten aufnimmst: Opus, MiniMax, Mimo haben Config; Haiku (durchgefallen) auch; Sonnet nicht. Konsens: 3/5 (modell-abhängig). Du entscheidest — wenn rein, dann mit der Begründung "Config ist Konvention, keine Architektur" oder "Config ist Architektur" und beides ist verteidigbar.

## Was du am Ende ablieferst

1. **12 (oder weniger) Knoten** mit: Label, Codestelle, 1-Satz-Bedeutung
2. **Kanten** zwischen Knoten, begründet
3. **3 Guided Views** ("01 Play story", "02 Play story", "03 Play story") — je 3–6 Schritte
4. **Liste der zusätzlich geöffneten Codestellen** (sollte ≤5 sein)
5. **Deine Auswahlbegründung** — pro Knoten eine Zeile: warum dieser, nicht jener

## Vergleichbarkeit

Deine Karte wird gegen `hai-mcp.architecture.opus.html` gehalten. Beide sind von Opus gebaut, eine aus dem Repo, eine aus der Vereinigung von fünf Blicken. Maße: Knotenzahl, Belege pro Knoten, Guided View Tiefe, Knoten-Überlappung mit Opus-Karte.

---

**Input-Quelle:** `hai-mcp.claims.md` (338 Zeilen, 37 Cluster)
**Deine Lese-Erlaubnis:** Diese Datei + gezielte Codestellen + max 5 zusätzliche Stellen
**Deine Schreib-Erlaubnis:** `hai-mcp.architecture.composed.html` + `.json`
