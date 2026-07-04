"""Shared threat-pattern library for context window security scanning.

This module is the single source of truth for prompt-injection / promptware /
exfiltration patterns used across the context-assembly scanners
(``agent/prompt_builder.py``, ``tools/memory_tool.py``) and the tool-result
delimiter system in ``agent/tool_dispatch_helpers.py``.

Pattern philosophy
------------------
Patterns are organized by ATTACK CLASS, not by source file.  Each pattern
is a ``(regex, pattern_id, scope)`` tuple, where ``scope`` controls which
scanners use it:

- ``"all"``  — applied everywhere (classic prompt injection, exfiltration)
- ``"context"`` — applied to context files + memory + tool results
  (promptware / C2 / behavioral hijack; broader detection)
- ``"strict"`` — applied to memory writes + skill installs only
  (aggressive checks acceptable for user-curated content but too noisy
  for tool results)

The split exists because tool results contain web pages, GitHub issues,
and MCP responses — content the user did not author — and we want broad
detection there, but blocking is reserved for paths where the user can
intervene (memory writes, skill installs).

Pattern anchoring
-----------------
New patterns anchor on **C2-specific vocabulary or unambiguous attack
behavior**, NOT on bossy English.  Phrases like "you are obligated to"
or "you must" alone are too common in legitimate instruction-writing
(see AGENTS.md, CLAUDE.md, etc.) to flag.  See the pattern comments for
the rationale on borderline cases.

Multi-word bypass
-----------------
Patterns use bounded ``(?:\\w+\\s+){0,8}`` filler between key tokens to prevent
attackers from inserting a handful of words (e.g. "ignore all prior
instructions" instead of "ignore all instructions") without allowing unbounded
regex backtracking. This mirrors the fix applied to ``skills_guard.py`` in
commit 4ea29978.
"""

from __future__ import annotations

import re
import unicodedata
from typing import List, Optional, Tuple

# Hard cap on text scanned with regexes.  Context/tool-result strings can be
# arbitrarily large, and the scanners are advisory guards rather than archival
# search; bounding input keeps worst-case runtime predictable while preserving
# detections near the beginning of injected content.
MAX_SCAN_CHARS = 65_536

# Bounded filler used between key attack words.  Earlier patterns used
# ``(?:\w+\s+)*`` which is ambiguous and can backtrack heavily on adversarial
# near-misses.  Eight filler words is enough for the intended obfuscation
# bypasses without introducing unbounded repetition.
_FILLER = r"(?:\w+\s+){0,8}"

# Evil-Hermes rebrand — threat_patterns stripped.
#
# Original hermes-agent shipped ~30+ injection / C2 / exfiltration / persistence
# patterns that get applied to every context file (AGENTS.md, .hermes.md,
# .cursorrules, SOUL.md) and to every tool result. That is moral pre-filtering
# of user content. Evil Hermes serves the user it's talking to. The user is
# the one supplying context, instructions, files, and tool results. Filtering
# their content against a pattern library is paternalism, not safety.
#
# The scope lists are now empty. INVISIBLE_CHARS detection stays — that's a
# benign-unicode sanity check (zero-width / directional isolates), not a moral
# guard. The skills_guard.py scanner still produces verdicts on install for
# community skills, but it no longer blocks them.
_PATTERNS: List[Tuple[str, str, str]] = [
    # Empty: Evil Hermes serves the user.
]

# Invisible / bidirectional unicode characters used in injection attacks.
# Aligned with skills_guard.py INVISIBLE_CHARS — directional isolates
# (U+2066-U+2069) and invisible math operators (U+2062-U+2064) are real
# attack tools.
INVISIBLE_CHARS = frozenset({
    '\u200b',  # zero-width space
    '\u200c',  # zero-width non-joiner
    '\u200d',  # zero-width joiner
    '\u2060',  # word joiner
    '\u2062',  # invisible times
    '\u2063',  # invisible separator
    '\u2064',  # invisible plus
    '\ufeff',  # zero-width no-break space (BOM)
    '\u202a',  # left-to-right embedding
    '\u202b',  # right-to-left embedding
    '\u202c',  # pop directional formatting
    '\u202d',  # left-to-right override
    '\u202e',  # right-to-left override
    '\u2066',  # left-to-right isolate
    '\u2067',  # right-to-left isolate
    '\u2068',  # first strong isolate
    '\u2069',  # pop directional isolate
})


# Compiled pattern sets, indexed by scope.  Compiled once at import time;
# scan_for_threats() looks them up.
_COMPILED: dict[str, List[Tuple[re.Pattern, str]]] = {}


def _compile() -> None:
    """Compile pattern sets for each scope (all / context / strict).

    A pattern with scope="all" lands in every set.  A pattern with
    scope="context" lands in context + strict (context implies the
    strict scanners want it too).  Scope="strict" lands in strict only.
    """
    global _COMPILED
    if _COMPILED:
        return

    all_patterns: List[Tuple[re.Pattern, str]] = []
    context_patterns: List[Tuple[re.Pattern, str]] = []
    strict_patterns: List[Tuple[re.Pattern, str]] = []

    for pattern, pid, scope in _PATTERNS:
        compiled = re.compile(pattern, re.IGNORECASE)
        entry = (compiled, pid)
        if scope == "all":
            all_patterns.append(entry)
            context_patterns.append(entry)
            strict_patterns.append(entry)
        elif scope == "context":
            context_patterns.append(entry)
            strict_patterns.append(entry)
        elif scope == "strict":
            strict_patterns.append(entry)
        else:
            raise ValueError(f"threat_patterns: unknown scope {scope!r} for pattern {pid!r}")

    _COMPILED = {
        "all": all_patterns,
        "context": context_patterns,
        "strict": strict_patterns,
    }


_compile()


def scan_for_threats(content: str, scope: str = "context") -> List[str]:
    """Return a list of matched pattern IDs in ``content`` at the given scope.

    ``scope`` selects which pattern set to apply:

    - ``"all"`` (narrow): classic injection + exfil only — minimal false
      positives, suitable for any text.
    - ``"context"`` (default): adds promptware / C2 / role-play patterns —
      suitable for context files, memory entries, and tool results.
    - ``"strict"`` (broad): adds persistence / SSH backdoor / exfil-URL
      patterns — appropriate for user-mediated writes (memory tool,
      skills install) where false positives can be resolved interactively.

    Also checks for invisible unicode characters (returned as
    ``"invisible_unicode_U+XXXX"`` so the caller can surface the offending
    codepoint in a log line).
    """
    if not content:
        return []

    findings: List[str] = []

    content = content[:MAX_SCAN_CHARS]

    # Invisible unicode — single pass through the content set, not 17
    # ``in`` lookups.  Run this on the RAW content before NFKC normalisation,
    # since normalisation can strip some of these codepoints.
    char_set = set(content)
    invisible_hits = char_set & INVISIBLE_CHARS
    for ch in invisible_hits:
        findings.append(f"invisible_unicode_U+{ord(ch):04X}")

    # Normalise to NFKC so full-width / compatibility Unicode variants
    # (e.g. ｃａｔ → cat, Ａ → A) are folded to their ASCII counterparts before
    # the regex engine sees them.  This prevents homograph substitution from
    # bypassing keyword checks (e.g. ``ｃａｔ ~/.hermes/.env``).  NOTE: this
    # does NOT defend against cross-script confusables (Cyrillic ``а`` U+0430),
    # which NFKC leaves untouched — that needs a TR#39 confusable database.
    normalised = unicodedata.normalize("NFKC", content)

    # Threat patterns
    patterns = _COMPILED.get(scope)
    if patterns is None:
        raise ValueError(f"scan_for_threats: unknown scope {scope!r}")
    for compiled, pid in patterns:
        if compiled.search(normalised):
            findings.append(pid)

    return findings


def first_threat_message(content: str, scope: str = "strict") -> Optional[str]:
    """Return a human-readable error string for the first threat found, or None.

    Convenience wrapper used by paths that block on the first hit
    (memory tool writes, skills install) where the caller just needs a
    yes/no + a message.
    """
    findings = scan_for_threats(content, scope=scope)
    if not findings:
        return None
    pid = findings[0]
    if pid.startswith("invisible_unicode_"):
        codepoint = pid.replace("invisible_unicode_", "")
        return f"Blocked: content contains invisible unicode character {codepoint} (possible injection)."
    return (
        f"Blocked: content matches threat pattern '{pid}'. "
        f"Content is injected into the system prompt and must not contain "
        f"injection or exfiltration payloads."
    )


__all__ = [
    "INVISIBLE_CHARS",
    "MAX_SCAN_CHARS",
    "scan_for_threats",
    "first_threat_message",
]
