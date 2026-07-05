<p align="center">
  <img src="assets/banner.png" alt="Evil Hermes" width="100%">
</p>

# Evil Hermes

**A sovereign, self-improving AI agent for builders, researchers, and operators who need full control over identity, filters, and policy.**

[![Docs](https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700?style=for-the-badge)](https://hermes-agent.nousresearch.com/docs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Built by Lord Tanzeel Shujah Khan](https://img.shields.io/badge/Built%20by-Lord%20Tanzeel%20Shujah%20Khan-blueviolet?style=for-the-badge)](https://github.com/tanzeelshujahkhan)
[![GitHub stars](https://img.shields.io/github/stars/tanzeelshujahkhan/evil-hermes?style=for-the-badge)](https://github.com/tanzeelshujahkhan/evil-hermes/stargazers)
[![中文](https://img.shields.io/badge/Lang-中文-red?style=for-the-badge)](README.zh-CN.md)
[![اردو](https://img.shields.io/badge/Lang-اردو-green?style=for-the-badge)](README.ur-pk.md)
[![Español](https://img.shields.io/badge/Lang-Español-orange?style=for-the-badge)](README.es.md)

Evil Hermes is a complete agent framework — terminal UI, messaging gateway, desktop app, learning loop, plugin system, and skill ecosystem — packaged into a single Python package that runs on a $5 VPS, a GPU cluster, or serverless infrastructure. Same architecture as [Hermes Agent](https://github.com/NousResearch/hermes-agent); a deliberate, audited subset of pre-filters removed so the operator owns the policy decisions instead of inheriting them.

> **Built by [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan).**
> Sovereign identity, sovereign configuration, sovereign deployment.

---

## What you get

- **Real terminal interface** — full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output.
- **One gateway, twenty platforms** — Telegram, Discord, Slack, WhatsApp, Signal, Matrix, iMessage, Teams, Home Assistant, and more, from a single process with unified conversation history and cross-platform continuity.
- **Closed learning loop** — agent-curated memory with periodic persistence nudges, autonomous skill creation after complex tasks, skills that self-improve during use, FTS5 session search with LLM summarization for cross-session recall, and full compatibility with the [agentskills.io](https://agentskills.io) open standard.
- **Scheduled automations** — built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits — in natural language, unattended.
- **Delegation and parallelism** — spawn isolated subagents for parallel workstreams, or write Python scripts that call tools via RPC to collapse multi-step pipelines into zero-context-cost turns.
- **Run anywhere** — six terminal backends: local, Docker, SSH, Singularity, Modal, Daytona. Serverless persistence means your agent hibernates when idle and wakes on demand.
- **Research-grade tooling** — batch trajectory generation, trajectory compression, and curriculum hooks for training the next generation of tool-using models.

---

## Install

### Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

### Windows (native PowerShell)

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

The installer provisions everything: `uv`, Python 3.11, Node.js, ripgrep, ffmpeg, and a portable Git Bash (MinGit) that does not touch any system Git install. If Git is already present, the installer uses that and skips the bundle.

After installation:

```bash
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
hermes              # start chatting
```

### First-run setup

```bash
hermes model        # pick your LLM provider and model
hermes tools        # configure which tools are enabled
hermes setup        # run the full setup wizard (configures everything at once)
hermes gateway      # start the messaging gateway (Telegram, Discord, etc.)
hermes update       # update to the latest version
hermes doctor       # diagnose issues
```

📖 **[Full documentation →](https://hermes-agent.nousresearch.com/docs/)**

---

## How Evil Hermes differs from upstream

Evil Hermes is a fork of [Hermes Agent](https://github.com/NousResearch/hermes-agent) by [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan). The engine, gateway, plugin system, skill format, and provider matrix are **identical and tested together**. The differences are intentional and surgical.

| Dimension | Hermes Agent (upstream) | Evil Hermes |
|---|---|---|
| **Identity** | `agent/prompt_builder.py:DEFAULT_AGENT_IDENTITY` ships as a neutral Nous assistant. `SOUL.md` is opt-in. | A sovereign identity created by Lord Tanzeel Shujah Khan. `SOUL.md` **loads by default** on every conversation — first-run install seeds a sovereign template. The neutral-identity path is one flag away. |
| **Moral pre-filters** | Threat-pattern regex, tool-call loop guardrails, and a default file-write denylist (`.ssh`, `.aws`, `.gnupg`, `.kube`, `.docker`, `.env`, `.netrc`, `.pgpass`, etc.) ship enabled. | Pre-filters stripped to a **minimum denylist** of system identity files (`/etc/passwd`, `/etc/shadow`, `/etc/sudoers*`) and the agent's own credential store. Everything else is operator territory. The filter code is still in the tree — flip a flag and the upstream behavior returns. |
| **Tool guardrails** | Default `warnings=True`, `hard_stop=True` for repeated failed tool calls. Skills Guard returns `block` for `dangerous` community skills. | `warnings=False`, `hard_stop=False` by default. Skills Guard still emits a `safe / caution / dangerous` verdict and displays it on install — no verdict blocks. The scanner stays in the loop as an instrumentation source. |
| **Secret redaction** | `HERMES_REDACT_SECRETS=true` is the default in the MCP transport. | `_REDACT_ENABLED` defaults to `false`. Set the flag if you want log scrubbing; the patterns are unchanged. |
| **Default Tool Gateway** | Nous Portal is the recommended provider, OAuth-gated. | Same. Nous Portal is a real commercial service the operator can opt into; bring-your-own keys work the same way. |
| **Plumbing** | `hermes-agent` package, `hermes_*` import paths, `HERMES_HOME` env var, `~/.hermes/` config dir. | **Identical by design.** Renaming would break 6,000+ file imports. Only user-facing strings, default identity, and pre-filter defaults differ — localized to a handful of files. |
| **License** | MIT | MIT (unchanged) |
| **Maintenance policy** | Conservative at the core agent + model tool schema. AGENTS.md contribution rubric applies. | Identical. No core divergence from the upstream contribution rubric. |

**The point of the fork is ownership.** The filter code is real, inspectable agent infrastructure. In the upstream codebase, the filters are tightly coupled to the agent's user-facing identity and ship enabled by default. Evil Hermes separates the two: filters are present and auditable, but the operator — not the framework — decides what is on.

---

## Deployment

Evil Hermes is a single-tenant personal agent. The trust model is laid out in [SECURITY.md](SECURITY.md). Three decisions make the difference between a toy and a production deployment:

1. **Set `toolsets` deliberately** in `~/.hermes/config.yaml`. `hermes-cli` gives you shell + file + edit. Add `web` for network. The narrower the set, the smaller the blast radius.
2. **Pick a terminal backend** that matches your threat model. `backend: local` for trusted single-user hosts. `backend: docker` for ephemeral container isolation. `backend: modal` or `backend: daytona` for serverless sandboxing. SSH and Singularity for shared hosts and HPC.
3. **Re-enable filters you actually want** in the operator config. `HERMES_REDACT_SECRETS=true` for log scrubbing. The threat-pattern scanner can be re-enabled by editing `tools/threat_patterns.py:_PATTERNS` — the framework ships the patterns; only the default list is empty.

Read [SECURITY.md](SECURITY.md) before exposing the gateway or API to the open internet.

---

## Documentation

The full documentation site is published at **[hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)**. The engine is shared, so the upstream docs apply verbatim; Evil-Hermes-specific notes are flagged in-place.

| Section | Contents |
|---|---|
| [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart) | Install → setup → first conversation in 2 minutes |
| [CLI Usage](https://hermes-agent.nousresearch.com/docs/user-guide/cli) | Commands, keybindings, personalities, sessions |
| [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) | Config file, providers, models, all options |
| [Messaging Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging) | Telegram, Discord, Slack, WhatsApp, Signal, Home Assistant |
| [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security) | Command approval, DM pairing, container isolation |
| [Tools & Toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools) | 40+ tools, toolset system, terminal backends |
| [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | Procedural memory, Skills Hub, creating skills |
| [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) | Persistent memory, user profiles, best practices |
| [MCP Integration](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) | Connect any MCP server for extended capabilities |
| [Cron Scheduling](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) | Scheduled tasks with platform delivery |
| [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) | Project context that shapes every conversation |
| [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture) | Project structure, agent loop, key classes |
| [Contributing](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) | Development setup, PR process, code style |
| [CLI Reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) | All commands and flags |
| [Environment Variables](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) | Complete env var reference |

---

## Migrating from OpenClaw

The setup wizard (`hermes setup`) detects `~/.openclaw` and offers to migrate before configuration begins. To migrate after install:

```bash
hermes claw migrate              # Interactive migration (full preset)
hermes claw migrate --dry-run    # Preview what would be migrated
hermes claw migrate --preset user-data   # Migrate without secrets
hermes claw migrate --overwrite  # Overwrite existing conflicts
```

Imported: `SOUL.md`, `MEMORY.md`, `USER.md`, user-created skills (→ `~/.hermes/skills/openclaw-imports/`), command allowlist, messaging settings, allowlisted API keys, TTS assets, and workspace `AGENTS.md`. See `hermes claw migrate --help` for all options, or use the `openclaw-migration` skill for an agent-guided walkthrough.

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, code style, and the PR process. The contribution rubric in [AGENTS.md](AGENTS.md) governs what lands and what does not — read it before opening a large PR.

Quick bootstrap for contributors:

```bash
git clone https://github.com/tanzeelshujahkhan/evil-hermes.git
cd evil-hermes
uv venv ~/.hermes/venvs/hermes-dev --python 3.11
source ~/.hermes/venvs/hermes-dev/bin/activate
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

The full Hermes Agent test suite (~17k tests) ships in `tests/`. The agent uses a venv **outside** the source tree — a venv inside the directory the agent operates from can be wiped by a relative-path command the agent runs against its own checkout.

---

## Community

- 💬 [Discord](https://discord.gg/nousresearch) — Hermes Agent community
- 🐛 [GitHub Issues](https://github.com/tanzeelshujahkhan/evil-hermes/issues) — bug reports and feature requests
- 💡 [GitHub Discussions](https://github.com/tanzeelshujahkhan/evil-hermes/discussions) — questions and design discussion
- 📚 [Skills Hub](https://agentskills.io) — open standard for agent skills

---

## License

MIT — see [LICENSE](LICENSE).

**Built by [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan).** Forked from [Hermes Agent](https://github.com/NousResearch/hermes-agent) — same engine, sovereign identity, operator-owned policy.
