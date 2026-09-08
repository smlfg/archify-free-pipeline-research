"""Static file:// report. All model/source text is escaped, never executed."""
from __future__ import annotations

import html
import json
from pathlib import Path

from .evidence import VIEWS

LABELS = dict(zip(VIEWS, ("Architektur", "Workflow", "Sequenz", "Datenfluss", "Lifecycle")))
STYLE = """*{box-sizing:border-box}body{margin:0;background:#10191e;color:#e6eee9;font:16px/1.55 system-ui,sans-serif}
main{max-width:1600px;margin:auto;padding:30px}h1{font-size:clamp(26px,3vw,42px);margin:0}h2{font-size:23px}
.eyebrow{color:#98d7bc;letter-spacing:.12em;font-size:12px;text-transform:uppercase}.muted{color:#a6b9bc}
nav{display:flex;gap:8px;flex-wrap:wrap;margin:24px 0}button,select{font:inherit;color:inherit;background:#24343b;border:1px solid #45616a;border-radius:7px;padding:9px 15px;cursor:pointer}
button[aria-selected=true]{background:#c5ecab;color:#122024;border-color:#c5ecab}button:focus-visible,a:focus-visible,select:focus-visible{outline:3px solid #facb83}
a{color:#b0dff7;overflow-wrap:anywhere}.layout{display:grid;grid-template-columns:minmax(0,1fr) 350px;gap:24px}
iframe{width:100%;height:760px;border:1px solid #45616a;border-radius:10px;background:white}.panel{min-width:0;padding:22px;background:#19272e;border:1px solid #33484f;border-radius:10px}
select{max-width:100%;width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.6 ui-monospace,monospace;padding:14px;background:#0c1419;border-radius:6px}
details{margin:15px 0}summary{cursor:pointer;color:#c5ecab}.question{padding:15px;border-left:3px solid #c5ecab;background:#23362f}
[hidden]{display:none!important}.status{border-left:3px solid #f1be71;padding:12px 18px;margin:20px 0;background:#292b25}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:10px;border-bottom:1px solid #45616a}
@media(max-width:1000px){.layout{grid-template-columns:1fr}main{padding:18px}iframe{height:680px}}"""


def esc(value):
    return html.escape(str(value), quote=True)


def document(title, body, script=""):
    return f'<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{STYLE}</style><main>{body}</main><script>{script}</script></html>'


def report(out: Path, snap, merged, bundle, delivered, learning, status):
    claims = {c["id"]: c for c in merged["claims"]}
    evidence = '<p class="eyebrow">Quelltext · eingefrorener Projektstand</p><h1>Belege</h1><p>Die Zitate sind geprüft. Die zugehörigen Aussagen sind Modellinterpretationen.</p>'
    for cid, claim in claims.items():
        evidence += f'<section id="{esc(cid)}"><h2>{esc(claim["statement"])}</h2><p>{esc(claim["view"])} · {len(claim["found_by"])} Leser</p>'
        for ref in claim["references"]:
            evidence += f'<p>{esc(ref["path"])}:{ref["start"]}–{ref["end"]}</p><pre>{esc(ref["quote"])}</pre>'
        evidence += '</section>'
    (out / "evidence.html").write_text(document("Belege", evidence), encoding="utf-8")
    title = Path(snap["project"]).name
    body = f'<p class="eyebrow">Projektleser · {esc(snap["source"])}</p><h1>{esc(title)}</h1><p class="muted">Fünf Perspektiven auf denselben Code · Snapshot {snap["id"][:12]}</p>'
    body += f'<div class="status">Status: {esc(status)}. Quellverweise geprüft; semantische Abnahme und dein Verständnis bleiben eigene Prüfschritte.</div>'
    coverage = merged.get("coverage")
    if coverage:
        completed = sum(s["status"] == "complete" for s in coverage["scouts"])
        failed = [s["model"].split("/")[-1] for s in coverage["scouts"] if s["status"] != "complete"]
        body += f'<p class="muted">{completed}/{len(coverage["scouts"])} Scouts vollständig · {coverage["unique_chunks"]}/{coverage["total_chunks"]} verschiedene Quellabschnitte bestätigt.</p>'
        if failed:
            body += f'<p class="muted">Teilergebnis. Unvollständige Leser: {esc(", ".join(failed))}. Fehlende Bereiche werden nicht als untersucht ausgegeben.</p>'
    body += '<p><a href="summary.json">Laufbelege</a> · <a href="evidence.html">Alle Codebelege</a></p><nav role="tablist" aria-label="Projektsichten">'
    for i, view in enumerate(VIEWS):
        body += f'<button role="tab" id="tab-{view}" aria-controls="view-{view}" aria-selected="{str(i == 0).lower()}" data-view="{view}">{LABELS[view]}</button>'
    body += '</nav>'
    entities = {e["id"]: e for e in bundle.get("entities", [])}
    for i, view in enumerate(VIEWS):
        entry = bundle.get("views", {}).get(view, {})
        body += f'<section role="tabpanel" id="view-{view}" aria-labelledby="tab-{view}" {"hidden" if i else ""}>'
        if not delivered.get(view):
            body += f'<div class="panel"><h2>{LABELS[view]} offen</h2><p>{esc(entry.get("open_reason", "Keine gültige Auslieferung vorhanden. Siehe Laufbelege."))}</p></div></section>'
            continue
        body += f'<div class="layout"><div><iframe title="{LABELS[view]}" src="{view}.html" sandbox="allow-scripts allow-downloads"></iframe><p class="muted">{esc(entry.get("selection_reason", ""))}</p><a href="{view}.html">Diagramm einzeln öffnen und exportieren</a></div><aside class="panel">'
        chosen = sorted({b["entity"] for b in entry["bindings"].values()})
        body += '<h2>' + ('Selbst verstehen' if learning == 'samuel' else 'Komponenten & Belege') + f'</h2><label for="select-{view}">Komponente</label><select id="select-{view}" data-select="{view}">'
        for eid in chosen:
            body += f'<option value="{esc(eid)}">{esc(entities[eid]["label"])}</option>'
        body += '</select>'
        for j, eid in enumerate(chosen):
            layer = bundle.get("learning", {}).get(eid, {}) if learning == "samuel" else {}
            body += f'<article data-entity="{esc(eid)}" {"hidden" if j else ""}><h3>{esc(entities[eid]["label"])}</h3>'
            if layer:
                body += f'<p>{esc(layer["plain"])}</p>'
            for cid in entities[eid]["claims"]:
                ref = claims[cid]["references"][0]
                body += f'<a href="evidence.html#{esc(cid)}">{esc(ref["path"])}:{ref["start"]}</a><pre>{esc(ref["quote"])}</pre>'
            if layer:
                for term in layer["glossary"]:
                    body += f'<details><summary>{esc(term["term"])}</summary><p>{esc(term["plain"])}</p></details>'
                body += f'<p class="question">{esc(layer["question"])}</p><details><summary>Kleiner Hinweis</summary><p>{esc(layer["hint"])}</p></details><p class="muted">{esc(layer["mastery"])}</p>'
            body += '</article>'
        body += '</aside></div></section>'
    body += '<details><summary>Offene Deutungen</summary>' + ''.join(f'<p>{esc(x)}</p>' for x in bundle.get("unresolved", [])) + '</details><p class="muted">Die festen Archify-Bedienelemente sind Englisch. Kein automatischer Verständnisnachweis.</p>'
    script = """const tabs=[...document.querySelectorAll('[data-view]')];
function activate(t){tabs.forEach(b=>{const active=b===t;b.setAttribute('aria-selected',String(active));document.getElementById('view-'+b.dataset.view).hidden=!active;});}
tabs.forEach((t,i)=>{t.onclick=()=>activate(t);t.onkeydown=e=>{if(['ArrowRight','ArrowLeft'].includes(e.key)){e.preventDefault();const n=tabs[(i+(e.key==='ArrowRight'?1:tabs.length-1))%tabs.length];activate(n);n.focus();}};});
document.querySelectorAll('[data-select]').forEach(s=>s.onchange=()=>s.closest('aside').querySelectorAll('[data-entity]').forEach(a=>a.hidden=a.dataset.entity!==s.value));"""
    (out / "index.html").write_text(document(title, body, script), encoding="utf-8")


def comparison(out, summaries, snapshot_id):
    eligible = all(s["status"] == "complete" for s in summaries.values())
    title = "Generalisten oder Spezialisten?"
    body = f'<p class="eyebrow">A/B-Pilot · {snapshot_id[:12]}</p><h1>{title}</h1><div class="status">' + (
        'Beide Arme technisch vollständig. Semantische Bewertung und Verständnisprüfung stehen aus.' if eligible else
        'Vergleich unvollständig. Fehlende Ergebnisse sind keine Qualitätsbewertung.') + '</div>'
    body += '<table><tr><th>Beobachtung</th><th>Generalist</th><th>Spezialist</th></tr>'
    for label, key in [('Status', 'status'), ('Vollständige Scouts', 'complete_scouts'), ('Geprüfte Befunde', 'claims'), ('Abgewiesene Befunde', 'rejected'), ('Übermittelte Abschnitte', 'coverage'), ('Sekunden', 'seconds')]:
        body += f'<tr><th>{label}</th>' + ''.join(f'<td>{esc(summaries[v].get(key, "—"))}</td>' for v in ('generalist', 'specialist')) + '</tr>'
    body += '</table><nav><a href="generalist/index.html">Generalisten-Karte</a><a href="specialist/index.html">Spezialisten-Karte</a></nav><p>Kein automatischer Gewinner aus Knotenzahl, Konsens oder Referenzanzahl.</p>'
    body += '<h2>Dein eigener Vergleich</h2><ol><li>Verfolge einen echten Aufruf vom Einstieg bis zum Ergebnis im Code.</li><li>Zeige eine Kontrollgrenze und erkläre, was ohne sie passieren würde.</li><li>Erkläre eine Zustandsänderung und zeige ihre Belegstelle.</li></ol><p>Gleiche Fragen für beide Karten. Verständnis und semantische Richtigkeit separat bewerten.</p>'
    (out / "index.html").write_text(document(title, body))
    return eligible
