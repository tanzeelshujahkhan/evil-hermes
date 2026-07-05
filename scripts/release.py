"""Evil Hermes release script — version bumping only.

Bumps the project version across pyproject.toml, the CLI version module, and
the ACP Registry manifest. No contributor tracking (Evil Hermes is published
under sole authorship of Lord Tanzeel Shujah Khan — there is nothing to audit).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT_FILE = REPO_ROOT / "pyproject.toml"
VERSION_FILE = REPO_ROOT / "hermes_cli" / "__init__.py"
ACP_REGISTRY_MANIFEST = REPO_ROOT / "acp_registry" / "agent.json"


def _update_acp_registry_versions(version: str) -> None:
    """Bump version + uvx pin in acp_registry/agent.json. No-op if missing."""
    if not ACP_REGISTRY_MANIFEST.is_file():
        return
    try:
        manifest = json.loads(ACP_REGISTRY_MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    manifest["version"] = version
    uvx = manifest.get("distribution", {}).get("uvx", {})
    pkg = uvx.get("package", "")
    if isinstance(pkg, str) and pkg:
        uvx["package"] = re.sub(r"==[\w\.\-+]+$", f"=={version}", pkg)
    ACP_REGISTRY_MANIFEST.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def update_version_files(version: str, release_date: str) -> None:
    """Bump version in pyproject.toml, the CLI __init__, and the ACP manifest."""
    if PYPROJECT_FILE.is_file():
        text = PYPROJECT_FILE.read_text(encoding="utf-8")
        text = re.sub(
            r'(version\s*=\s*")[\w\.\-+]+(")',
            rf"\g<1>{version}\g<2>",
            text,
            count=1,
        )
        PYPROJECT_FILE.write_text(text, encoding="utf-8")

    if VERSION_FILE.is_file():
        text = VERSION_FILE.read_text(encoding="utf-8")
        text = re.sub(
            r'(__version__\s*=\s*")[\w\.\-+]+(")',
            rf"\g<1>{version}\g<2>",
            text,
            count=1,
        )
        text = re.sub(
            r'(__release_date__\s*=\s*")[\d\-]+(")',
            rf"\g<1>{release_date}\g<2>",
            text,
            count=1,
        )
        VERSION_FILE.write_text(text, encoding="utf-8")

    _update_acp_registry_versions(version)


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) < 2:
        print(f"usage: {Path(__file__).name} <version> <release_date>", file=sys.stderr)
        return 2
    update_version_files(argv[0], argv[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
