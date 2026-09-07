#!/bin/sh

set -eu

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATOR="$ROOT/scripts/validate_skill.py"
RELEASE_RUNNER="$ROOT/scripts/release.py"

fail() {
  echo "rfstack check failed: $*" >&2
  exit 1
}

command -v uv >/dev/null 2>&1 || fail "uv is required"
[ -x "$VALIDATOR" ] || fail "skill validator must be executable"
[ -x "$RELEASE_RUNNER" ] || fail "release runner must be executable"
sh -n "$ROOT/scripts/check.sh"

for skill_dir in "$ROOT"/skills/*; do
  [ -d "$skill_dir" ] || continue
  "$VALIDATOR" "$skill_dir"
done

PYTHONDONTWRITEBYTECODE=1 uv run --no-project --python 3.11 python - "$ROOT" <<'PY'
from pathlib import Path
import re
import sys
import tomllib

root = Path(sys.argv[1])
version = (root / "VERSION").read_text().strip()
if not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", version):
    raise SystemExit("VERSION must contain a stable SemVer core such as 1.2.3")

with (root / "release.toml").open("rb") as stream:
    config = tomllib.load(stream)

release = config.get("release", {})
if release.get("name") != "rfstack":
    raise SystemExit("release.name must be rfstack")
if release.get("version_source") != "VERSION":
    raise SystemExit("release.version_source must be VERSION")
if release.get("runner_protocol") != "prepared-v1":
    raise SystemExit("release.runner_protocol must be prepared-v1")
if release.get("runner", [])[:4] != [
    "uv", "run", "scripts/release.py", "version-file-release"
]:
    raise SystemExit("release.runner must use the checked-in version-file runner")
if "--check" in release.get("runner", []):
    raise SystemExit("checks must be declared once in [checks].commands")
if release.get("dry_run_args") != ["--dry-run"]:
    raise SystemExit("release.dry_run_args must enable the runner dry-run")
if release.get("publish") is not True:
    raise SystemExit("release.publish must be true")
if config.get("checks", {}).get("commands") != [["./scripts/check.sh"]]:
    raise SystemExit("release checks must use ./scripts/check.sh")

source = config.get("runner_source", {})
if source.get("repository") != "https://github.com/iancleary/release-skills":
    raise SystemExit("runner_source.repository must identify release-skills")
if not re.fullmatch(r"[0-9a-f]{40}", source.get("revision", "")):
    raise SystemExit("runner_source.revision must be a full Git commit")
if not re.fullmatch(r"[0-9a-f]{64}", source.get("sha256", "")):
    raise SystemExit("runner_source.sha256 must be a SHA-256 digest")

compile((root / "scripts/release.py").read_text(), "scripts/release.py", "exec")
compile((root / "scripts/validate_skill.py").read_text(), "scripts/validate_skill.py", "exec")
PY

"$RELEASE_RUNNER" --help >/dev/null
PYTHONDONTWRITEBYTECODE=1 \
  env -u VIRTUAL_ENV uv run --project "$ROOT/skills/rfschemdraw" \
  python -m unittest discover -s "$ROOT/skills/rfschemdraw/tests"
git -C "$ROOT" diff --check

echo "rfstack checks passed"
