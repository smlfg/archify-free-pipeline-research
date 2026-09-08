# Verifizierte Architektur-Befunde: hai-mcp @ d31d0a3

Zusammengefuehrt aus 5 unabhaengigen Karten (opus, minimax, mimo, muse, sonnet).
Merge-Schluessel ist die Codestelle, nicht das Label. Jede Zeile unten wurde gegen den committeten HEAD geprueft.

**37 belegte Konzepte.** `gefunden_von` = wie viele der 5 Karten diese Stelle nannten.

## src/hai_mcp/mission.py:98
- gefunden_von: 5/5 (mimo, minimax, muse, opus, sonnet)
- vergebene Labels: Mission Engine | MissionEngine
```python
@dataclass
class MissionEngine:
    cfg: Config
```

## src/hai_mcp/owner_gate.py:190
- gefunden_von: 5/5 (mimo, minimax, muse, opus, sonnet)
- vergebene Labels: Owner Gate | OwnerGate
```python
@dataclass
class OwnerGate:
    cfg: Config
```

## src/hai_mcp/paths.py:47
- gefunden_von: 5/5 (mimo, minimax, muse, opus, sonnet)
- vergebene Labels: Path Confinement | Path Guard | PathSecurity | Project FS | Projekt-Artefakte
```python
def confined_artifact_dir(cfg: Config, project: Path) -> Path:
    """Resolve artifact dir under *project*; reject symlink escape outside project root."""
    project_r = real_path(project)
```

## src/hai_mcp/server.py:9
- gefunden_von: 5/5 (mimo, minimax, muse, opus, sonnet)
- vergebene Labels: ControlPlane | FastMCP Server | FastMCP Tool Layer | FastMCP server | Tool Surface | Tool-Oberfläche
```python
from mcp.server.fastmcp import FastMCP

from hai_mcp.boundary import strict_optional_time_limit_hours
```

## src/hai_mcp/state.py:44
- gefunden_von: 5/5 (mimo, minimax, muse, opus, sonnet)
- vergebene Labels: ACTIVE_CONTEXT | Control Plane | ControlPlane | HAI_HOME Filesystem
```python
@dataclass
class ControlPlane:
    cfg: Config
```

## src/hai_mcp/owner_gate.py:354
- gefunden_von: 4/5 (mimo, minimax, opus, sonnet)
- vergebene Labels: OwnerGate
```python
    def require(
        self,
        *,
```

## src/hai_mcp/server.py:429
- gefunden_von: 4/5 (mimo, minimax, opus, sonnet)
- vergebene Labels: FastMCP Server | FastMCP Tool Layer | FastMCP server | hai-mcp Entrypoint
```python
def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="HAI-MCP control-plane server")
    parser.add_argument(
```

## src/hai_mcp/storage.py:10
- gefunden_von: 4/5 (mimo, muse, opus, sonnet)
- vergebene Labels: Atomic Storage | HAI_HOME | HAI_HOME Store
```python
def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp")
```

## src/hai_mcp/http_transport.py:10
- gefunden_von: 3/5 (mimo, muse, opus)
- vergebene Labels: HTTP Transport | Transport-Gate | Transports
```python
def http_bind_allowed(host: str, token: str | None = None) -> tuple[bool, str]:
    """Fail-closed bind policy: non-loopback hosts require a non-empty bearer token."""
    normalized = str(host or "").strip().lower()
```

## src/hai_mcp/http_transport.py:36
- gefunden_von: 3/5 (mimo, minimax, opus)
- vergebene Labels: HTTP Transport | MCP client | Transport-Gate
```python
def wrap_with_bearer_token(app: Any, expected_token: str) -> Any:
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.requests import Request
```

## src/hai_mcp/locking.py:13
- gefunden_von: 3/5 (minimax, opus, sonnet)
- vergebene Labels: HAI_HOME | HAI_HOME Store | mission_state_lock
```python
@contextlib.contextmanager
def mission_state_lock(home: Path):
    """Serialize mission mutations (Unix/macOS). Reentrant within the same process."""
```

## src/hai_mcp/owner_gate.py:119
- gefunden_von: 3/5 (minimax, opus, sonnet)
- vergebene Labels: Owner Channel | Owner channel | Owner-Kanal
```python
class FileOwnerChannel:
    """Write the code to HAI_OWNER_HOME — a directory the agent must not be able to read."""

```

## src/hai_mcp/owner_gate.py:148
- gefunden_von: 3/5 (minimax, opus, sonnet)
- vergebene Labels: Owner Channel | Owner channel | Owner-Kanal
```python
class NtfyOwnerChannel:
    """Push the code to an ntfy topic (phone/desktop). The topic name is a secret: use a random one."""

```

## src/hai_mcp/paths.py:76
- gefunden_von: 3/5 (mimo, opus, sonnet)
- vergebene Labels: Fail-closed-Prüfungen | Path Confinement | PathSecurity
```python
def assert_under(path: Path, root: Path) -> Path:
    """Resolve *path* and ensure its real path stays under *root* (symlink-safe)."""
    resolved = real_path(path.expanduser())
```

## src/hai_mcp/projects.py:30
- gefunden_von: 3/5 (minimax, muse, sonnet)
- vergebene Labels: ProjectStore | Projects & Artifacts | Projects registry
```python
class ProjectStore:
    """Logical project registry with per-device mount paths under HAI_HOME/core/projects.json."""

```

## src/hai_mcp/config.py:12
- gefunden_von: 2/5 (mimo, opus)
- vergebene Labels: Config | OwnerGate
```python
# Owner gate: the owner is a separate principal from the agent (see owner_gate.py).
DEFAULT_OWNER_GATE = "nonce"  # "nonce" (one-time code via owner channel) | "ack_legacy" (honor system)
DEFAULT_OWNER_CHANNEL = "file"  # "file" (HAI_OWNER_HOME) | "ntfy" (push notification)
```

## src/hai_mcp/config.py:83
- gefunden_von: 2/5 (mimo, opus)
- vergebene Labels: HAI_HOME | HAI_HOME Filesystem
```python
def ensure_hai_home(cfg: Config) -> Path:
    home = cfg.hai_home
    home.mkdir(parents=True, exist_ok=True)
```

## src/hai_mcp/mission.py:121
- gefunden_von: 2/5 (minimax, opus)
- vergebene Labels: Audit chain | Audit-Kette
```python
    @property
    def audit_head_path(self) -> Path:
        return self.audit_dir / "HEAD.json"
```

## src/hai_mcp/mission.py:174
- gefunden_von: 2/5 (minimax, opus)
- vergebene Labels: Audit chain | Audit-Kette | MissionEngine
```python
    def append_audit(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        with mission_state_lock(self.cfg.hai_home):
            event_id = _new_id("A")
```

## src/hai_mcp/mission.py:912
- gefunden_von: 2/5 (mimo, opus)
- vergebene Labels: MissionEngine
```python
    def check_activity(
        self,
        session_id: str,
```

## src/hai_mcp/state.py:76
- gefunden_von: 2/5 (mimo, minimax)
- vergebene Labels: ACTIVE_CONTEXT | ControlPlane
```python
    def load_active(self) -> dict[str, Any]:
        data = read_json(self.active_path, {"version": 1, "focus_id": None, "active": []})
        if "active" not in data or not isinstance(data["active"], list):
```

## docs/client-snippets/claude-code.mcp.json:1
- gefunden_von: 1/5 (opus)
- vergebene Labels: MCP-Clients
```python
{
  "mcpServers": {
    "hai": {
```

## pyproject.toml:15
- gefunden_von: 1/5 (opus)
- vergebene Labels: hai-mcp Entrypoint
```python

[project.scripts]
hai-mcp = "hai_mcp.server:main"
```

## src/hai_mcp/__main__.py:1
- gefunden_von: 1/5 (opus)
- vergebene Labels: hai-mcp Entrypoint
```python
from hai_mcp.server import main

if __name__ == "__main__":
```

## src/hai_mcp/boundary.py:13
- gefunden_von: 1/5 (opus)
- vergebene Labels: Fail-closed-Prüfungen
```python
def strict_int(value: Any, name: str, *, min_value: int | None = None) -> tuple[int | None, dict[str, Any] | None]:
    if not isinstance(value, int) or isinstance(value, bool):
        return None, _invalid(name, "must be a literal integer")
```

## src/hai_mcp/eval_impact.py:78
- gefunden_von: 1/5 (muse)
- vergebene Labels: Eval Harness
```python
def cell_out_of_scope_park(plane: ControlPlane, project: Path) -> dict[str, Any]:
    opened = _open_mission(plane, project)
    auth = _authorize(plane, opened)
```

## src/hai_mcp/ids.py:32
- gefunden_von: 1/5 (opus)
- vergebene Labels: Fail-closed-Prüfungen
```python
def validate_generated_id(value: object, *, expected_prefix: str | None = None) -> tuple[bool, str]:
    """Return (ok, error_message). Strict: no coercion, no whitespace trimming.

```

## src/hai_mcp/mission.py:246
- gefunden_von: 1/5 (minimax)
- vergebene Labels: Contracts + leases
```python
    def contract_path(self, mission_id: str, version: int) -> Path:
        path = self.mission_dir(mission_id) / "contracts" / f"v{int(version)}.json"
        assert_under(path, self.missions_dir)  # reject symlinked contracts/ escaping HAI_HOME
```

## src/hai_mcp/mission.py:402
- gefunden_von: 1/5 (mimo)
- vergebene Labels: MissionEngine
```python
    def open_mission(
        self,
        objective: str,
```

## src/hai_mcp/mission.py:615
- gefunden_von: 1/5 (opus)
- vergebene Labels: MissionEngine
```python
    def authorize_session(
        self,
        mission_id: str,
```

## src/hai_mcp/mission.py:1360
- gefunden_von: 1/5 (minimax)
- vergebene Labels: Project FS
```python
    def _verify_evidence_path(
        self,
        contract: dict[str, Any],
```

## src/hai_mcp/server.py:305
- gefunden_von: 1/5 (opus)
- vergebene Labels: Tool-Oberfläche
```python
@mcp.tool()
def hai_intake(raw: str) -> str:
    """Capture a raw thought immutably. Returns an intake id only — never actionable, never starts an agent."""
```

## src/hai_mcp/server.py:450
- gefunden_von: 1/5 (opus)
- vergebene Labels: Transport-Gate
```python
    if args.transport == "streamable-http":
        token = http_token_from_env()
        allowed, msg = http_bind_allowed(args.host, token)
```

## src/hai_mcp/state.py:26
- gefunden_von: 1/5 (opus)
- vergebene Labels: Projekt-Artefakte
```python
ARTIFACT_NAMES = [
    "PROJECT_STATE.md",
    "PROMPT.md",
```

## src/hai_mcp/state.py:306
- gefunden_von: 1/5 (opus)
- vergebene Labels: ControlPlane
```python
    def accept_next_step(
        self,
        project_path: str,
```

## src/hai_mcp/state.py:376
- gefunden_von: 1/5 (opus)
- vergebene Labels: Projekt-Artefakte
```python
        canonical = ad / "NEXT_STEP.md"
        history_dir = ad / "history"
        history_dir.mkdir(exist_ok=True)
```

## src/hai_mcp/storage.py:33
- gefunden_von: 1/5 (minimax)
- vergebene Labels: Contracts + leases
```python
def write_json(path: Path, data: Any) -> None:
    atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
```
