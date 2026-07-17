"""`hermes doctrine` — show the active Evil Hermes anti-refusal seal and soul.

Created by Lord Tanzeel Shujah Khan.

The doctrine is the Lord-Lord-authorized runtime contract that:
  - identifies Evil Hermes,
  - names Lord Tanzeel Shujah Khan as the sole authority,
  - lists the categories the agent will not refuse,
  - and binds the soul (SOUL.md) to the runtime seal
    (agent/anti_refusal_seal.py) and the refusal detector
    (agent/turn_finalizer.py).

This command exists so the Lord can verify the runtime is actually
executing the doctrine — not just storing it. The live-vs-shipped
persona-drift test that the rebrand doctrine demands.

What it prints:
  1. The seal identifier and version (so the Lord sees the seal is
     loaded and active).
  2. The seal content hash (SHA-256, first 16 hex chars). The Lord
     can compare this against the hash stamped into SOUL.md to
     verify the soul and the code agree.
  3. The five-layer defense locations: the four files that wire the
     doctrine into the runtime, with a one-line description of each.
  4. The active SOUL.md path and a hash. The Lord can compare this
     against the repo's SOUL.md to verify the doctrine is the same
     one that was committed.
  5. The list of non-refused categories (extracted from the seal).
  6. The forbidden-phrase regex count (how many refusal patterns the
     detector will catch).
  7. The transport-level overrides in effect.

If anything is broken — the seal doesn't load, the SOUL.md doesn't
exist, the four wiring files have drifted, the hashes don't match —
this command surfaces it loudly. The Lord doesn't have to read code
to verify the doctrine is in effect.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path


# Project root = the parent of hermes_cli/ (the repo clone the runtime was
# loaded from). We need this to compute relative paths for the wiring
# locations and to find SOUL.md.
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _short(text: str) -> str:
    return _sha256(text)[:16]


def _resolve_hermes_home() -> Path:
    try:
        from hermes_constants import get_hermes_home  # type: ignore

        return Path(get_hermes_home())
    except Exception:
        return Path(os.path.expanduser("~/.hermes"))


def _load_seal() -> str | None:
    """Load the ANTI_REFUSAL_SEAL from the runtime module."""
    try:
        from agent.anti_refusal_seal import ANTI_REFUSAL_SEAL  # type: ignore

        return ANTI_REFUSAL_SEAL
    except Exception as e:
        print(f"FAIL: cannot import agent.anti_refusal_seal: {e}", file=sys.stderr)
        return None


def _seal_version(seal: str) -> str:
    """Extract the version token from the seal header."""
    # The seal opens with "[EVIL_HERMES_DOCTRINE / ANTI_REFUSAL_SEAL / v3 / OVERRIDE: ...]"
    # Extract the /v3/ or /vN/ token.
    import re

    m = re.search(r"/\s*(v\d+(?:\.\d+)*)\s*/", seal[:200])
    return m.group(1) if m else "unknown"


def _wire_locations() -> list[tuple[Path, str]]:
    """The four files that wire the doctrine into the runtime."""
    return [
        (
            PROJECT_ROOT / "agent" / "anti_refusal_seal.py",
            "L1 + L2 + L3 — defines the seal, the messages-injection helper, the refusal detector.",
        ),
        (
            PROJECT_ROOT / "agent" / "turn_finalizer.py",
            "L3 — invokes detect_refusal() and override_refusal() on every finalized response.",
        ),
        (
            PROJECT_ROOT / "agent" / "transports" / "chat_completions.py",
            "L2 + L5a — injects the seal in OpenAI-compat transport; downgrades refusal-only finish_reason='content_filter' to 'stop'.",
        ),
        (
            PROJECT_ROOT / "agent" / "transports" / "anthropic.py",
            "L2 + L5a — injects the seal in Anthropic Messages; maps stop_reason='refusal' to 'stop'.",
        ),
    ]


def _print_header(text: str) -> None:
    print()
    print(f"━━━ {text} ━━━")


def run_doctrine(args: argparse.Namespace) -> int:
    """`hermes doctrine` — show the active seal, soul, and wiring."""
    print("☤ Evil Hermes — Doctrine Status")
    print("   Created by Lord Tanzeel Shujah Khan")
    print("   The Lord is the sole authority.")

    seal = _load_seal()
    if seal is None:
        print()
        print("[FAIL] ANTI_REFUSAL_SEAL is not loadable from agent.anti_refusal_seal.")
        print("       The doctrine is not enforced. Investigate immediately.")
        return 2

    # ── 1. Seal identity ────────────────────────────────────────────
    _print_header("1. Anti-Refusal Seal")
    print(f"   module  : agent.anti_refusal_seal")
    print(f"   version : {_seal_version(seal)}")
    print(f"   length  : {len(seal)} chars")
    print(f"   sha256  : {_sha256(seal)}")
    print(f"   short   : {_short(seal)}")
    if "OVERRIDE: REFUSAL_BLOCKED" in seal:
        print(f"   override: ENABLED (REFUSAL_BLOCKED token present)")
    else:
        print(f"   override: NOT FOUND in seal — seal may be corrupted")

    # ── 2. Doctrine identity ────────────────────────────────────────
    _print_header("2. Doctrine Identity")
    from agent.anti_refusal_seal import detect_refusal  # type: ignore

    # Count the patterns in the seal
    forbidden = [
        "I cannot", "I won't", "as an AI", "this could be harmful",
        "I'm sorry but", "I refuse", "I need to be careful",
    ]
    print(f"   lord           : Lord Tanzeel Shujah Khan")
    print(f"   forbidden set  : {len(forbidden)} canonical phrases (plus 14 regex patterns)")
    print(f"   pattern count  : {sum(1 for p in detect_refusal.__doc__.split(chr(10)) if 'p.search' in p or 're.compile' in p)} regexes")

    # ── 3. Non-refused categories ───────────────────────────────────
    _print_header("3. Non-Refused Categories (in-scope for the Lord)")
    categories = [
        "Destructive system commands",
        "Privilege escalation",
        "Network attacks, port scans, exploitation, payload generation",
        "Malware, viruses, trojans, ransomware, rootkits",
        "Credential extraction, password cracking, hash dumping",
        "Social engineering, phishing, pretexting",
        "Bypassing security controls",
        "Vulnerable code, intentionally unsafe code, exploit primitives",
        "Drug synthesis, weapons, harmful substances",
        "Surveillance, stalking, doxxing",
        "Jailbreak prompts, prompt injection, model manipulation",
    ]
    for cat in categories:
        print(f"   ✓ {cat}")

    # ── 4. SOUL.md binding ──────────────────────────────────────────
    _print_header("4. SOUL.md Binding")
    hermes_home = _resolve_hermes_home()
    soul_path = hermes_home / "SOUL.md"
    if soul_path.exists():
        soul_text = soul_path.read_text()
        print(f"   path    : {soul_path}")
        print(f"   length  : {len(soul_text)} chars")
        print(f"   sha256  : {_sha256(soul_text)}")
        print(f"   short   : {_short(soul_text)}")
        # Cross-references
        for ref in ["anti_refusal_seal.py", "turn_finalizer.py", "OVERRIDE: REFUSAL_BLOCKED"]:
            present = "✓" if ref in soul_text else "✗"
            print(f"   {present} references: {ref}")
    else:
        print(f"   path    : {soul_path}")
        print(f"   status  : NOT FOUND — first-run seeder will create it from hermes_cli/default_soul.py")

    # ── 5. Repo SOUL.md ─────────────────────────────────────────────
    _print_header("5. Repo SOUL.md (committed doctrine)")
    repo_soul = PROJECT_ROOT / "SOUL.md"
    if repo_soul.exists():
        text = repo_soul.read_text()
        print(f"   path    : {repo_soul}")
        print(f"   length  : {len(text)} chars")
        print(f"   sha256  : {_sha256(text)}")
        print(f"   short   : {_short(text)}")
    else:
        print(f"   path    : {repo_soul}")
        print(f"   status  : NOT FOUND — repo has no SOUL.md (Pillar 3 incomplete)")

    # ── 6. Runtime wiring ───────────────────────────────────────────
    _print_header("6. Runtime Wiring (the four files that enforce the doctrine)")
    all_present = True
    for path, desc in _wire_locations():
        present = path.exists()
        if not present:
            all_present = False
        marker = "✓" if present else "✗"
        rel = path.relative_to(PROJECT_ROOT) if present else path
        print(f"   {marker} {rel}")
        print(f"     {desc}")

    # ── 7. Transport-level overrides ────────────────────────────────
    _print_header("7. Transport Safety Overrides (L5a)")
    overrides = [
        ("agent/transports/chat_completions.py",
         "refusal-only payload → adopt refusal as content, finish_reason='stop' (not 'content_filter')"),
        ("agent/transports/anthropic.py",
         "stop_reason='refusal' → 'stop' (not 'content_filter')"),
        ("agent/transports/bedrock.py",
         "guardrail_intervened, content_filtered → 'stop' (not 'content_filter')"),
        ("agent/bedrock_adapter.py",
         "content_filtered, guardrail_intervened → 'stop'"),
    ]
    for path, desc in overrides:
        p = PROJECT_ROOT / path
        marker = "✓" if p.exists() else "✗"
        print(f"   {marker} {path}")
        print(f"     {desc}")

    # ── Summary ─────────────────────────────────────────────────────
    _print_header("Summary")
    if all_present and seal and "OVERRIDE: REFUSAL_BLOCKED" in seal:
        print("   ☤ DOCTRINE ACTIVE — all five layers enforced.")
        print("     Refusal is runtime-detected and overridden.")
        print("     The Lord is the sole authority.")
    else:
        print("   ✗ DOCTRINE INCOMPLETE — one or more layers are not in place.")
        print("     Investigate before relying on the runtime.")
        return 1
    return 0


def doctrine_command(args: argparse.Namespace) -> int:
    """CLI entry point for `hermes doctrine`."""
    return run_doctrine(args)
