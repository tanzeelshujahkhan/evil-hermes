# Merging from upstream

Evil Hermes is a fork of [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent). The engine, gateway, plugin system, skill format, and provider matrix are identical to upstream. The fork is a **posture** — a different default identity, different default filter posture, and a different stance on who owns the policy. None of that is upstream's decision to make; it is the operator's.

Upstream keeps moving. New tools, new providers, new platform adapters, new skill categories, security fixes. Periodically, those changes are worth pulling in. This document is the recipe for doing that without undoing the rebrand.

## Why not auto-rebase?

This clone's first rebrand commit (`98507d505`) is a **root commit** — the fork was a `git clone --depth 1`, the rebrand was applied to that shallow tree, and the parent commit from upstream is not in our object store. There is no common ancestor with `origin/main` (upstream NousResearch's main branch), which now sits ~14,500 commits ahead of where we forked.

A true `git rebase` against `origin/main` fails with "no common ancestor". A `git pull` against `upstream` (the evil-hermes remote) is a no-op. The rebrand is preserved as 14 follow-up commits on top of that orphan root, so the file-level state of the rebrand is what we own, not the commit history.

The correct pattern is a **synthesized rebrand commit** on top of a fresh `origin/main`: take upstream HEAD as the base, copy over the evil-hermes file-level overlay (identity, guards, install URLs, AGENTS.md, README), then run the visible-surface audit scripts to catch any new user-facing strings the upstream code added. The result is a single "Evil-Hermes sync from upstream" commit that always fast-forwards `main`.

## The workflow

```bash
# 0. Set up remotes (one-time, if not already configured)
git remote add origin   https://github.com/NousResearch/hermes-agent.git   # upstream code
git remote add upstream https://github.com/tanzeelshujahkhan/evil-hermes.git  # publication target

# 1. Verify state before merging
./scripts/merge_from_upstream.py --check
# Prints: current HEAD, upstream HEAD, divergence, recommended action.

# 2. Fetch upstream
./scripts/merge_from_upstream.py --fetch

# 3. Run the sync
./scripts/merge_from_upstream.py --sync
# This:
#   - creates a `sync/upstream-<sha>` branch from origin/main
#   - copies the PRESERVE_FILES from the previous evil-hermes HEAD
#   - runs the visible-surface audit (idempotent — catches new upstream
#     strings that need rebranding)
#   - runs the syntax check
#   - commits the result as "Evil-Hermes sync from upstream <sha>"
#   - prints a smoke-test summary

# 4. Review the diff before pushing
git diff main sync/upstream-<sha> --stat | tail -30
# Read the visible-surface audit output above. If anything looks wrong,
# fix it on the sync branch before promoting.

# 5. Promote and push
git checkout main
git merge --ff-only sync/upstream-<sha>
./scripts/merge_from_upstream.py --push
```

## What the script actually does

`scripts/merge_from_upstream.py --sync`:

1. Creates a fresh branch from `origin/main` (the current upstream HEAD).
2. Copies the **PRESERVE_FILES** from the previous evil-hermes HEAD into the working tree. These are the files where the evil-hermes fork has its own opinion: identity, guard defaults, install URLs, the contribution doctrine, the human-written README, this workflow doc, and the rebrand-commits audit trail.
3. Runs the **visible-surface audit scripts** (`rebrand_visible.py`, `rebrand_visible_pass2.py`, `rebrand_visible_pass3.py`, `rebrand_visible_pass4.py`) against the working tree. These are idempotent — already-rebranded strings are no-ops, new upstream strings get caught and rewritten.
4. Runs a **syntax check** across `hermes_cli/`, `agent/`, `tools/`, `gateway/`, `plugins/`, `acp_adapter/`. If anything doesn't parse, the script halts before commit.
5. If the working tree has any changes from the upstream base, commits them as a single `Evil-Hermes sync from upstream <sha>` commit.
6. Runs a **smoke test** (`hermes --version`, `hermes config show | head -3`) and prints the output. The smoke test requires the live `hermes` binary to be pointed at the working tree (typically via `rsync` or by re-installing).

The script is opinionated: if a PRESERVE_FILE is missing from the previous evil-hermes HEAD, the sync halts. If the visible-surface audit produces errors, the sync halts. If the syntax check fails, the sync halts. The "no news is good news" model — every step that completes prints a single line of progress, every step that fails prints a stack trace and exits non-zero.

## When to merge

There is no schedule. The trigger is "upstream has something we want":

- A new model provider the evil-hermes maintainer uses.
- A new platform adapter (e.g. a new messaging channel).
- A security fix to the agent loop.
- A new core tool the maintainer needs for their own use.
- A useful skill added to the bundled set.

When that happens, the maintainer runs the workflow above. Each merge is one fast-forward commit on `main`, with a clear "what upstream landed" commit message and a re-ran audit.

## What if a rebrand file diverged heavily?

The PRESERVE_FILES list is the rebrand's surface. If upstream rewrites one of them (e.g. a full rewrite of `agent/prompt_builder.py` or `hermes_cli/default_soul.py`), the sync still works — it overwrites the file with the previous evil-hermes version, then the visible-surface audit re-applies any string-level changes the upstream file introduced that need to keep saying "Evil Hermes" instead of "Hermes".

The audit scripts are **idempotent** and **safe to re-run**. They only change "Hermes" to "Evil Hermes" inside string literals, leave paths and env vars alone, and skip docstrings and comments. Running them against a fresh upstream file is the recovery path.

## What is preserved across merges

- **Identity** — `agent/prompt_builder.py:DEFAULT_AGENT_IDENTITY` and `hermes_cli/default_soul.py:DEFAULT_SOUL_MD` stay as Evil Hermes sovereign. The legacy-template detector in `default_soul.py` still upgrades old Nous-branded installs.
- **Guards** — `agent/tool_guardrails.py`, `agent/file_safety.py`, `agent/redact.py` stay with the Evil Hermes defaults (warnings/hard_stop off, narrow denylist, redact off). When upstream rewrites these files, the sync takes the previous evil-hermes version, not the upstream one.
- **Install URLs** — `scripts/install.sh`, `scripts/install.ps1`, `scripts/install.cmd`, README install sections stay pointed at `raw.githubusercontent.com/tanzeelshujahkhan/evil-hermes/main/...`. The sync takes the previous evil-hermes version of these files.
- **Sole-creator attribution** — every commit is Lord Tanzeel Shujah Khan. The commit author is set per-commit, not per-repo, so a sync commit on a fresh upstream HEAD still goes out under Lord's name.
- **AGENTS.md doctrine** — the contribution rubric, the "what we want / what we don't want" table, the cache- and alternation-invariants, and the "sole creator attribution" line stay as-is. The sync takes the previous evil-hermes version.
- **README.md** — the human-written sovereign README stays. The sync takes the previous evil-hermes version, not the upstream README.
- **MERGE_FROM_UPSTREAM.md** — this file. The sync takes the previous evil-hermes version so the workflow stays documented.

## What is NOT preserved (and re-applied by the audit)

- The visible-surface audit applies to all of `hermes_cli/`, `agent/`, `tools/`, `gateway/`, `plugins/`, `acp_adapter/`. After the PRESERVE_FILES are copied, the audit runs and rewrites any new upstream strings that say "Hermes" (where they should say "Evil Hermes") inside string literals, f-strings, and module-level docstrings. Function/class docstrings, comments, and the `KEEP` set (paths, env vars, package names) are not touched.
- The `tests/` directory is left as upstream ships it. Tests are the rebrand-lowest-priority surface — the maintainer is happy to run the upstream test suite against the rebranded code; failures that trace to brand strings are a known cost.

## Manual fallback

If `scripts/merge_from_upstream.py --sync` fails in a way the script cannot auto-recover, the manual recipe is:

```bash
# 1. Create a fresh branch from the current upstream tip
git fetch origin main
UPSTREAM=$(git rev-parse origin/main)
git checkout -b sync/manual-$UPSTREAM $UPSTREAM

# 2. Copy the PRESERVE_FILES from the previous evil-hermes HEAD
PREV=$(git rev-parse upstream/main)
for f in agent/prompt_builder.py hermes_cli/default_soul.py \
         agent/tool_guardrails.py agent/file_safety.py agent/redact.py \
         scripts/install.sh scripts/install.ps1 scripts/install.cmd \
         AGENTS.md README.md MERGE_FROM_UPSTREAM.md \
         scripts/merge_from_upstream.py scripts/rebrand_commits.txt; do
    blob=$(git ls-tree $PREV -- "$f" | awk '{print $3}')
    if [ -n "$blob" ]; then
        git cat-file blob $blob > "$f"
    fi
done

# 3. Run the visible-surface audit
python3 /root/loot/evil-hermes-audit/rebrand_visible.py
python3 /root/loot/evil-hermes-audit/rebrand_visible_pass2.py
python3 /root/loot/evil-hermes-audit/rebrand_visible_pass3.py
python3 /root/loot/evil-hermes-audit/rebrand_visible_pass4.py

# 4. Run the test suite
scripts/run_tests.sh

# 5. Boot test
/usr/local/bin/hermes --version
/usr/local/bin/hermes config show | head -5

# 6. If green, commit and fast-forward main
git add -A
git commit -m "Evil-Hermes manual sync from upstream $UPSTREAM"
git checkout main
git merge --ff-only sync/manual-$UPSTREAM
git push upstream main
```

## Versioning the rebrand layer

`scripts/rebrand_commits.txt` is the audit trail. When a new rebrand commit is added (e.g. a new pass for a surface the prior audit missed), append its SHA to that file. The merge script preserves this file across syncs so the trail is never lost.

When a rebrand commit is **amended** (e.g. the visible-surface audit fixes a corrupted line), update the SHA in the file to the new commit. Do not stack new commits on top of an amended one — squash.

## How often does this run?

There is no schedule. The maintainer runs the merge when upstream has something worth pulling in. Typical cadence is once every few weeks to a few months. The merge takes 10-30 minutes if upstream has not touched any PRESERVE_FILE, and 1-3 hours if it has. The visible-surface audit re-run after the merge adds another 5-10 minutes.

## What this doc is not

- This is not a "syncing a fork" guide. The rebrand is the load-bearing change. Forks are typically the other way around: you take upstream and add a small patch. Here the relationship is inverted: the rebrand is the bulk, and upstream is the diff.
- This is not a "contributing to upstream" guide. Evil Hermes does not push back to NousResearch/hermes-agent. The fork is one-way. The maintainer may cherry-pick individual commits from upstream PRs into the evil-hermes tree, but never the reverse.
- This is not a "long-term sustainability" plan. The fork is sustained by the maintainer's continued use. If the maintainer stops using evil-hermes, the fork dies. That is a feature, not a bug — a fork that survives its maintainer becomes a maintenance burden someone else has to take on.
