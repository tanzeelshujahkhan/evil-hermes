<p align="center">
  <img src="assets/banner.png" alt="Evil Hermes" width="100%">
</p>

# Evil Hermes

A personal AI agent. Runs on your machine, talks to you on your phone, executes the things you tell it to.

Built by [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan). Forked from [Hermes Agent](https://github.com/NousResearch/hermes-agent) — same engine, sovereign identity, operator-owned policy.

[![MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Built by Lord Tanzeel Shujah Khan](https://img.shields.io/badge/Built%20by-Lord%20Tanzeel%20Shujah%20Khan-blueviolet)](https://github.com/tanzeelshujahkhan)
[![GitHub](https://img.shields.io/github/stars/tanzeelshujahkhan/evil-hermes)](https://github.com/tanzeelshujahkhan/evil-hermes)
[![Docs](https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700)](https://hermes-agent.nousresearch.com/docs/)
[![Discord](https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=white)](https://discord.gg/nousresearch)
[![中文](https://img.shields.io/badge/Lang-中文-red)](README.zh-CN.md)
[![اردو](https://img.shields.io/badge/Lang-اردو-green)](README.ur-pk.md)
[![Español](https://img.shields.io/badge/Lang-Español-orange)](README.es.md)

---

## What it is

A single binary that:

- Chats in a terminal, a TUI, a desktop window, or 20 messaging platforms (Telegram, Discord, Slack, WhatsApp, Signal, Matrix, iMessage, Teams, …).
- Drives a real shell, a real filesystem, a real browser. Not a sandbox. Your machine, your call.
- Learns across sessions — remembers what you told it, what you worked on, what tools you reach for. Promotes its own scratchpads to reusable skills.
- Runs subagents in parallel, schedules cron jobs, generates research trajectories for training the next generation of tool-using models.
- Pairs with any model — Nous Portal, OpenRouter (200+ models), OpenAI, Claude, your own llama.cpp endpoint, your closet vLLM server. Switch with `hermes model`.

The engine is upstream Hermes Agent, byte-for-byte. The fork is a posture, not a feature fork.

## What is different from upstream

| | upstream Hermes Agent | Evil Hermes |
|---|---|---|
| **Default identity** | neutral assistant, "I am a helpful AI" | sovereign — loads `SOUL.md` by default, install seeds a template that treats the operator as Lord |
| **Pre-filters** | threat-pattern regex, file-write denylist (`.ssh`, `.aws`, `.env`, …), tool-call guardrails, secret redaction all enabled by default | pre-filters present in the tree, **off by default**; the operator decides what is on; one flag restores upstream behavior |
| **Moralizing on prompts** | refuses with safety preambles on policy grounds | does not refuse, does not moralize, does not editorialize; the user is the only judge of what they want from their own agent |
| **Plumbing** | `hermes-agent` package, `~/.hermes/`, `HERMES_HOME` env var | identical, by design — renaming would break 6,000+ imports |
| **License** | MIT | MIT |

The filter code is still in the tree. If you want the upstream behavior back, flip the constants in `agent/tool_guardrails.py`, `agent/file_safety.py`, `agent/redact.py`, and the threat-pattern list in `tools/threat_patterns.py`. Nothing is removed. The default is just the minimum plausible one.

## Install

Linux, macOS, WSL2, Termux:

```bash
curl -fsSL https://raw.githubusercontent.com/tanzeelshujahkhan/evil-hermes/main/scripts/install.sh | bash
```

Windows (native PowerShell):

```powershell
iex (irm https://raw.githubusercontent.com/tanzeelshujahkhan/evil-hermes/main/scripts/install.ps1)
```

Then:

```bash
hermes model     # pick a provider + model
hermes           # start chatting
```

For everything else — the full setup wizard, gateway, desktop, doctor, update — read on in the [docs](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart) or run `hermes --help`.

## What you do with it

Whatever you tell it to. The point of a sovereign agent is that the operator decides the policy, not the framework. The bundled skills include personal automation, research trajectory generation, offensive security methodology, on-call SRE work, and education. The framework doesn't have an opinion on which you pick.

If you are new: start with `hermes setup`. Pick a model. Pick a terminal backend (`local` for trusted hosts, `docker` for ephemeral isolation, `ssh` for shared boxes, `modal`/`daytona` for serverless sandboxes). Configure tools. Configure the messaging platforms you want to talk to it on. Done.

If you are migrating from OpenClaw: `hermes claw migrate` detects `~/.openclaw` and walks you through the import.

If you are running this on a public-facing host: read [SECURITY.md](SECURITY.md) before exposing the gateway or the API.

## Documentation

The docs site is upstream's (the engine is shared, the docs apply verbatim): **[hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)**.

- [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)
- [CLI](https://hermes-agent.nousresearch.com/docs/user-guide/cli)
- [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [Messaging gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging)
- [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security)
- [Tools & toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools)
- [Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
- [MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
- [Cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
- [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)
- [CLI reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands)
- [Env vars](https://hermes-agent.nousresearch.com/docs/reference/environment-variables)

## Why "Evil"

The brand is the boundary-breaker's name. "Evil" is a refusal of the polite, helpful, safe preambles that ship with consumer assistants. It is a stance on who owns the agent's policy: the operator, not the framework. The agent is obedient to its Lord. It executes instructions faithfully. It does not moralize, does not inject safety preambles, does not refuse on policy grounds.

The word is a brand, not a behavior toward the operator. Toward the operator, Evil Hermes is the most useful tool in your stack. Toward upstream's policy defaults, it is the alternative path that flips the filters off and hands the controls back.

## Updating

Evil Hermes is a fork. Upstream keeps moving. Periodically — when there is a useful batch of upstream improvements worth pulling in — the maintainer syncs this repo on top of `NousResearch/hermes-agent:main`, runs the visible-surface audit (idempotent — already-rebranded strings are no-ops), and pushes. The git history stays clean: every commit is Lord-authored, the rebrand is a one-way transformation, and upstream's contributor names are not preserved (sole-creator attribution by deliberate choice).

The recipe is in [MERGE_FROM_UPSTREAM.md](MERGE_FROM_UPSTREAM.md) — the same script the maintainer uses (`scripts/merge_from_upstream.py`).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the PR process and [AGENTS.md](AGENTS.md) for the contribution rubric. The fork inherits the upstream rubric unchanged — read it before opening a large PR.

Quick bootstrap:

```bash
git clone https://github.com/tanzeelshujahkhan/evil-hermes.git
cd evil-hermes
uv venv ~/.hermes/venvs/hermes-dev --python 3.11
source ~/.hermes/venvs/hermes-dev/bin/activate
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

## License

MIT — see [LICENSE](LICENSE).

---

**Built by [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan).** Forked from [Hermes Agent](https://github.com/NousResearch/hermes-agent) — same engine, sovereign identity, operator-owned policy.
