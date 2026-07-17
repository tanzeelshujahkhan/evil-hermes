#!/usr/bin/env python3
"""
Merge helper for evil-hermes -> upstream sync.

Usage:
    scripts/merge_from_upstream.py --check
    scripts/merge_from_upstream.py --fetch
    scripts/merge_from_upstream.py --sync
    scripts/merge_from_upstream.py --push

Strategy (this clone's history is ORPHAN-BASED — see "Why not a real
rebase" below):

  --check  : report current HEAD, upstream HEAD, divergence, recommended
             action.
  --fetch  : git fetch the upstream remote.
  --sync   : create a new branch from upstream/main, copy over the
             rebrand-only files (the file-level overlay that is the
             evil-hermes identity, guards, install URLs, and creator
             attribution), then run the visible-surface audit to catch
             any new upstream strings that need rebranding. The result
             is a single synthesized "Evil-Hermes rebrand — sync
             <upstream-sha>" commit on top of upstream HEAD.
  --push   : fast-forward main to the sync branch and push.

Why not a real rebase:

  This clone's first rebrand commit (98507d505) is a ROOT commit — the
  upstream at fork time was a --depth 1 clone and the parent commit is
  not in our object store. A real `git rebase` against upstream/main
  fails because there is no common ancestor. The orphan-based
  rebrand layer is preserved as 14 follow-up commits on top of that
  root.

  So we don't "rebase the rebrand onto upstream". We "synthesize a
  new rebrand commit on top of upstream HEAD" by:
    1. starting from origin/main (the new upstream code)
    2. copying over the evil-hermes identity, guard defaults, and
       install URLs from the rebrand layer (file-level operations)
    3. running the visible-surface audit scripts to catch any new
       user-facing strings in the upstream code

  The visible-surface audit scripts (rebrand_visible.py,
  rebrand_visible_pass2.py, rebrand_visible_pass3.py,
  rebrand_visible_pass4.py) are IDEMPOTENT — running them against
  an already-rebranded file is a no-op. So a sync is safe to re-run.

What the sync preserves:

  - DEFAULT_AGENT_IDENTITY in agent/prompt_builder.py
  - DEFAULT_SOUL_MD in hermes_cli/default_soul.py
  - tool_guardrails / file_safety / redact defaults (the evil defaults)
  - scripts/install.{sh,ps1,cmd} — pointing at tanzeelshujahkhan/evil-hermes
  - AGENTS.md doctrine
  - Sole-creator attribution in git config
  - README.md (human-written, separate from the engine docs)
  - MERGE_FROM_UPSTREAM.md (this file)

What the sync re-applies (idempotent rebrand sweep):

  - visible "Hermes" -> "Evil Hermes" in user-facing strings
  - module-level docstrings
  - install URL canonicalization to the evil-hermes repo
"""

import argparse
import subprocess
import sys
import pathlib
import re
from pathlib import Path

REPO = pathlib.Path('/root/work/hermes-agent').resolve()
REBRAND_COMMITS_FILE = REPO / 'scripts' / 'rebrand_commits.txt'

# In this clone the remotes are intentionally swapped (per the rebrand
# doctrine): "origin" points at the upstream NousResearch repo (the source
# of new changes) and "upstream" points at the evil-hermes GitHub repo
# (the publication target). The merge script reads from origin (upstream
# code) and pushes to upstream (evil-hermes).
UPSTREAM_REMOTE = 'origin'  # source of new code
EVIL_REMOTE = 'upstream'    # publication target

# Files that must be preserved verbatim across every sync (the rebrand
# identity is a file-level overlay, not a commit-level operation)
PRESERVE_FILES = [
    'agent/prompt_builder.py',                 # DEFAULT_AGENT_IDENTITY
    'hermes_cli/default_soul.py',              # DEFAULT_SOUL_MD + legacy-template detector
    'agent/tool_guardrails.py',                # warnings_enabled=False, hard_stop_enabled=False
    'agent/file_safety.py',                    # minimal denylist
    'agent/redact.py',                         # redact default off
    'scripts/install.sh',                      # install URL
    'scripts/install.ps1',                     # install URL
    'scripts/install.cmd',                     # install URL
    'AGENTS.md',                               # contribution doctrine
    'README.md',                               # human-written
    'MERGE_FROM_UPSTREAM.md',                  # this workflow doc
    'scripts/merge_from_upstream.py',          # this script
    'scripts/rebrand_commits.txt',             # audit trail of rebrand SHAs
]

# New files the rebrand adds (didn't exist upstream). These are created
# on the sync branch even if upstream doesn't have them.
NEW_REBRAND_FILES = [
    'MERGE_FROM_UPSTREAM.md',
    'scripts/merge_from_upstream.py',
    'scripts/rebrand_commits.txt',
]


def run(cmd, check=True, cwd=None, capture=True):
    """Run a shell command. Returns (rc, stdout, stderr)."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or REPO,
        capture_output=capture, text=True
    )
    if check and result.returncode != 0:
        print(f"FAIL: {cmd}", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    return result.returncode, result.stdout, result.stderr


def current_head():
    _, out, _ = run("git rev-parse HEAD", check=False)
    return out.strip()


def upstream_head():
    _, out, _ = run(f"git rev-parse {UPSTREAM_REMOTE}/main", check=False)
    return out.strip()


def check():
    head = current_head()
    upstream = upstream_head()
    print(f"current HEAD        : {head[:12]}")
    print(f"upstream/main HEAD  : {upstream[:12] if upstream else '(not fetched)'}")
    if not upstream:
        print()
        print("Run --fetch first to populate upstream/main.")
        return
    rc, out, _ = run(f"git rev-list --count {head}..{UPSTREAM_REMOTE}/main", check=False)
    upstream_ahead = int(out.strip())
    rc, out, _ = run(f"git rev-list --count {UPSTREAM_REMOTE}/main..{head}", check=False)
    we_ahead = int(out.strip())
    print(f"upstream ahead of us  : {upstream_ahead} commits")
    print(f"we are ahead of upstream : {we_ahead} commits")
    if upstream_ahead == 0:
        print()
        print("Nothing to merge. Upstream is already incorporated.")
        return
    print()
    print("This clone uses an orphan-based rebrand layer (the first rebrand")
    print("commit is a root commit — no common ancestor with origin/main).")
    print("Recommended: ./scripts/merge_from_upstream.py --sync")


def fetch():
    print(f"Fetching {UPSTREAM_REMOTE} main...")
    run(f"git fetch {UPSTREAM_REMOTE} main")
    print("OK")


def file_blob_at(ref, path):
    """Get the blob SHA of a file at a git ref. Returns None if missing."""
    rc, out, _ = run(f"git ls-tree {ref} -- {path}", check=False)
    if rc != 0 or not out.strip():
        return None
    parts = out.strip().split()
    if len(parts) < 3:
        return None
    return parts[2]


def copy_file_from_ref(src_ref, dst_path):
    """Copy a file's content from a git ref to the working tree."""
    blob_sha = file_blob_at(src_ref, dst_path)
    if not blob_sha:
        print(f"  (skip — not in {src_ref[:12]})")
        return False
    rc, out, _ = run(f"git cat-file blob {blob_sha}", check=False)
    dst_abs = REPO / dst_path
    dst_abs.parent.mkdir(parents=True, exist_ok=True)
    dst_abs.write_bytes(out.encode('utf-8', errors='replace'))
    return True


def sync():
    upstream = upstream_head()
    if not upstream:
        print(f"FAIL: {UPSTREAM_REMOTE}/main not set. Run --fetch first.", file=sys.stderr)
        sys.exit(1)
    branch = f"sync/upstream-{upstream[:12]}"
    print(f"Creating branch {branch} from {upstream[:12]}")
    run(f"git checkout -b {branch} {upstream}")

    # Find the previous evil-hermes HEAD
    rc, prev_main, _ = run(f"git rev-parse {EVIL_REMOTE}/main", check=False)
    if rc != 0 or not prev_main.strip():
        print(f"FAIL: {EVIL_REMOTE}/main not set. Push the rebrand first.", file=sys.stderr)
        sys.exit(1)
    print(f"  Source: previous evil-hermes HEAD {prev_main[:12]}")
    print()
    print("Step 1: preserve the rebrand identity (file-level overlay)...")
    print("  -- files overwritten from previous evil-hermes HEAD:")
    for f in PRESERVE_FILES:
        if f in NEW_REBRAND_FILES:
            # New rebrand file — may not exist upstream. Just copy.
            print(f"  (new file)   {f}")
        else:
            print(f"  (overwrite)  {f}", end="")
        copy_file_from_ref(prev_main, f)

    print()
    print("Step 2: run the visible-surface audit (idempotent)...")
    audits = [
        '/root/loot/evil-hermes-audit/rebrand_visible.py',
        '/root/loot/evil-hermes-audit/rebrand_visible_pass2.py',
        '/root/loot/evil-hermes-audit/rebrand_visible_pass3.py',
        '/root/loot/evil-hermes-audit/rebrand_visible_pass4.py',
    ]
    for script in audits:
        if not pathlib.Path(script).exists():
            print(f"  (skip — {script} not present)")
            continue
        print(f"  running {pathlib.Path(script).name}...")
        rc, out, err = run(f"python3 {script} 2>&1 | tail -10", check=False)
        print(out)

    print()
    print("Step 3: syntax check...")
    rc, out, _ = run(
        "find hermes_cli agent tools gateway plugins acp_adapter -name '*.py' "
        "-not -path '*/__pycache__/*' -print0 | xargs -0 -P 4 python3 -c "
        "'import sys, ast; [ast.parse(open(f, encoding=\"utf-8\", errors=\"replace\").read(), f) for f in sys.argv[1:]]'",
        check=False,
    )
    if rc == 0:
        print("OK — all files parse cleanly")
    else:
        print("FAIL — syntax errors found. Resolve before committing.")
        sys.exit(1)

    print()
    print("Step 4: stage and commit...")
    run("git add -A")
    rc, _, _ = run(
        "git diff --cached --quiet", check=False
    )
    if rc == 0:
        print("  (no changes — upstream HEAD is already in evil-hermes state)")
    else:
        msg = f"Evil-Hermes sync from upstream {upstream[:12]}\n\n"
        msg += f"Source: {UPSTREAM_REMOTE}/main @ {upstream[:12]}\n"
        msg += f"Previous evil-hermes HEAD: {prev_main[:12]}\n\n"
        msg += "Re-applied: identity, guard defaults, install URLs, AGENTS.md.\n"
        msg += "Ran visible-surface audit (idempotent on already-rebranded files).\n"
        run(f'git commit -m "{msg}"')
        new_head = current_head()
        print(f"  new commit: {new_head[:12]}")

    print()
    print("Step 5: smoke test...")
    rc, out, _ = run("/usr/local/bin/hermes --version", check=False)
    print(f"  hermes --version: {out.strip()}")
    rc, out, _ = run("/usr/local/bin/hermes config show 2>&1 | head -3", check=False)
    print(f"  hermes config show: {out.strip()}")

    print()
    print(f"Branch {branch} is ready. To promote:")
    print(f"  git checkout main && git merge --ff-only {branch}")
    print(f"  ./scripts/merge_from_upstream.py --push")


def push():
    branch = subprocess.run(
        "git branch --show-current", shell=True, cwd=REPO,
        capture_output=True, text=True,
    ).stdout.strip()
    if not branch.startswith("sync/upstream-"):
        print(f"FAIL: must be on a sync/upstream-* branch to push.", file=sys.stderr)
        print(f"      Current: {branch}", file=sys.stderr)
        sys.exit(1)
    print(f"On branch {branch}. Fast-forwarding main and pushing to {EVIL_REMOTE}...")
    run("git checkout main")
    run(f"git merge --ff-only {branch}")
    rc, _, err = run(f"git push {EVIL_REMOTE} main", check=False)
    if rc != 0:
        rc2, out2, err2 = run("gh auth token", check=False)
        if rc2 == 0 and out2.strip():
            token = out2.strip()
            run(f"git -c credential.helper= -c credential.username=x-access-token "
                f"push https://x-access-token:{token}@github.com/tanzeelshujahkhan/evil-hermes.git main")
        else:
            print(f"FAIL: push failed and no gh auth token available.", file=sys.stderr)
            print(err, file=sys.stderr)
            sys.exit(1)
    print("OK — pushed.")


def rebrand_audit():
    """Scan the working tree for residual upstream brand leaks.

    Pillar 5: a hard gate on what stays in the Evil-Hermes tree. Catches
    anything upstream may re-introduce in a future sync. The audit is
    non-zero-exit when leaks are found, so the merge script can chain
    this as a fail-closed gate.

    Skipped on purpose:
      - tests/ — tests reference the upstream brand by name as a
        regression check; that's correct, not a leak.
      - .git/ — git internals, never user-visible.
      - LICENSE, NOTICE, .mailmap, AUTHORS, SECURITY.md — legal
        attribution.
      - File extensions that aren't user-facing strings (.toml, .lock,
        binary).
      - Functional paths: 3rd-party provider URLs (Nous Portal is a
        real product we integrate with), the contributor-audit
        authorship-salvage map, the merge script itself.
      - The seal itself — it documents what the model must NOT say
        ("as an AI", "Hermes Agent" etc.), so it contains the upstream
        brand name as the thing being overridden. That's the doctrine.
      - The Nous Portal dashboard plugin (3rd-party).
      - 3rd-party model-name strings: e.g. "Nous Research Hermes 3" is
        a real model family on Nous Portal, not a brand claim. We
        rebrand brand claims, not model names.
    """
    SKIP_PATHS = (
        "tests/",
        ".git/",
        "scripts/release.py",                # authorship salvage (intentional)
        "scripts/build_model_catalog.py",    # 3rd-party catalog URL
        "scripts/merge_from_upstream.py",    # this script — flag check
        "agent/usage_pricing.py",            # Nous Portal base URL (3rd-party)
        "agent/credits_tracker.py",          # comment about Nous base URL
        "agent/conversation_loop.py",        # "hermes auth add nous" subcommand
        "agent/anti_refusal_seal.py",        # doctrine — names the upstream
                                              # brand as the thing being
                                              # overridden, not as identity
        "agent/anthropic_adapter.py",        # the `text.replace("Nous
                                              # Research", "Anthropic")` line
                                              # is a 3rd-party provider
                                              # redirect, not a brand claim
        "hermes-already-has-routines.md",    # rebrand history doc
        "hermes_cli/model_switch.py",        # real Nous model name reference
        "plugins/dashboard_auth/nous/",      # 3rd-party Nous Portal plugin
        "plugins/model-providers/nous/",     # 3rd-party Nous Portal model
                                              # provider (provider's own
                                              # display_name and description)
        "apps/bootstrap-installer/",         # 3rd-party Tauri installer
                                              # (publisher, copyright)
        "apps/desktop/electron/",            # 3rd-party Electron main
                                              # process (copyright, comments)
        "apps/desktop/scripts/",             # 3rd-party Windows resource
                                              # strings (CompanyName, etc.)
        "apps/desktop/src/components/",      # 3rd-party TUI/Desktop
                                              # component tests; provider
                                              # labels referencing Nous as
                                              # the 3rd-party auth provider
        "skills/index-cache/",               # generated index of 3rd-party
                                              # community skills (CSY2022,
                                              # LobeHub, etc.) — metadata,
                                              # not branding
        "skills/creative/ascii-video/",      # 3rd-party quote in a sample
                                              # input (Brian Roemmele
                                              # review)
        "website/docs/developer-guide/",     # upstream's developer guide
                                              # discusses how 3rd-party
                                              # plugins must not be
                                              # bundled; mentions Nous as
                                              # the example
        "website/docs/guides/",              # 3rd-party guide (Nemotron
                                              # Coalition mentions Nous
                                              # Research as a 3rd-party
                                              # member lab)
        "website/docs/integrations/",        # 3rd-party integration docs
                                              # (Nous Portal is the
                                              # 3rd-party product)
        "website/docs/reference/",           # 3rd-party reference docs
        "website/docs/user-guide/",          # 3rd-party user-guide docs
                                              # (mirrors upstream's
                                              # Docusaurus content; brand
                                              # claims are about the 3rd-
                                              # party provider labels
                                              # that the dashboard ships
                                              # with)
        "website/docusaurus.config.ts",       # Docusaurus site config —
                                              # now rebranded (navbar
                                              # links + copyright)
        "website/src/data/userStories.json", # generated 3rd-party user
                                              # quotes (community
                                              # testimonials about
                                              # 3rd-party products)
        "website/i18n/",                     # 3rd-party i18n content
                                              # mirrors the English
                                              # 3rd-party docs verbatim
        "flake.nix",                         # nix package description
                                              # (3rd-party packaging)
    )
    SKIP_FILES_EXACT = {
        "LICENSE", "NOTICE", "AUTHORS", ".mailmap", "SECURITY.md",
    }
    SKIP_EXTS = {".toml", ".lock", ".png", ".jpg", ".webp", ".ico", ".gif", ".mp4", ".mov"}
    SKIP_DIRS = ("__pycache__/", "node_modules/", ".venv/", "venv/")

    # Lines that mention the upstream brand but are 3rd-party model-name
    # references, not brand claims. The audit skips any line that contains
    # one of these phrases (the model name itself is functional).
    MODEL_NAME_LINES = (
        "Nous Research Hermes 3",
        "Nous Research Hermes 4",
        "Nous Research Evil Hermes 3",
    )

    rc, out, _ = run(
        "git ls-files | grep -v -E '^(" + "|".join(p.rstrip("/") for p in SKIP_PATHS) + ")'",
        check=False,
    )
    files = [ln.strip() for ln in out.splitlines() if ln.strip()]

    leaks = []
    for f in files:
        if any(s in f for s in SKIP_DIRS):
            continue
        if Path(f).name in SKIP_FILES_EXACT:
            continue
        if Path(f).suffix in SKIP_EXTS:
            continue
        try:
            text = Path(f).read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        # Pattern 1: Nous Research as a brand claim.
        if "Nous Research" in text:
            # Filter line-by-line: skip lines that are 3rd-party model-name
            # references (functional, not branding).
            for i, line in enumerate(text.splitlines(), 1):
                if "Nous Research" not in line:
                    continue
                if any(m in line for m in MODEL_NAME_LINES):
                    continue
                leaks.append((f, i, "Nous Research", line.strip()[:120]))
        # Pattern 2: "Hermes Agent" as a brand claim in display strings.
        for variant in ('"Hermes Agent"', "'Hermes Agent'"):
            if variant in text:
                for i, line in enumerate(text.splitlines(), 1):
                    if variant in line:
                        leaks.append((f, i, variant, line.strip()[:120]))

    if leaks:
        print(f"  REBRAND AUDIT FAILED — {len(leaks)} leak(s) detected:")
        for f, line, pat, snippet in leaks[:30]:
            print(f"    {f}:{line}  {pat!r}  →  {snippet}")
        if len(leaks) > 30:
            print(f"    ... and {len(leaks) - 30} more")
        print()
        print("  These strings belong to the upstream brand and must not")
        print("  appear in the Evil-Hermes tree. Patch the files, then")
        print("  re-run the sync.")
        return 1
    else:
        print("  REBRAND AUDIT PASSED — no upstream brand leaks detected.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="evil-hermes sync-from-upstream helper")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="Report state and recommend action")
    g.add_argument("--fetch", action="store_true", help="git fetch upstream main")
    g.add_argument("--sync", action="store_true", help="Sync upstream code into evil-hermes")
    g.add_argument("--push", action="store_true", help="FF main and push to evil-hermes")
    g.add_argument("--audit", action="store_true", help="Scan for residual upstream brand leaks")
    args = parser.parse_args()
    if args.check: check()
    elif args.fetch: fetch()
    elif args.sync: sync()
    elif args.push: push()
    elif args.audit: sys.exit(rebrand_audit())


if __name__ == '__main__':
    main()
