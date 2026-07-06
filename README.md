<p align="center">
  <img src="assets/banner.png" alt="Evil Hermes" width="100%">
</p>

# Evil Hermes

**A sovereign, self-improving AI agent framework — built for operators who need full control over identity, filters, and policy.**

[![Docs](https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700?style=for-the-badge)](https://hermes-agent.nousresearch.com/docs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Built by Lord Tanzeel Shujah Khan](https://img.shields.io/badge/Built%20by-Lord%20Tanzeel%20Shujah%20Khan-blueviolet?style=for-the-badge)](https://github.com/tanzeelshujahkhan)
[![GitHub stars](https://img.shields.io/github/stars/tanzeelshujahkhan/evil-hermes?style=for-the-badge)](https://github.com/tanzeelshujahkhan/evil-hermes/stargazers)
[![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/nousresearch)
[![中文](https://img.shields.io/badge/Lang-中文-red?style=for-the-badge)](README.zh-CN.md)
[![اردو](https://img.shields.io/badge/Lang-اردو-green?style=for-the-badge)](README.ur-pk.md)
[![Español](https://img.shields.io/badge/Lang-Español-orange?style=for-the-badge)](README.es.md)

> **Built by [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan).**
> Sovereign identity. Sovereign configuration. Sovereign deployment.

---

## What is Evil Hermes?

Evil Hermes is a **complete AI agent framework** that runs the same engine across a CLI, a messaging gateway (Telegram, Discord, Slack, WhatsApp, Signal, Matrix, iMessage, Teams, Home Assistant, and more), a terminal UI, and a native desktop app. It learns across sessions, delegates to subagents, runs scheduled jobs, and drives a real terminal and browser.

It is a **fork of [Hermes Agent](https://github.com/NousResearch/hermes-agent)** by [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan). The engine, gateway, plugin system, skill format, and provider matrix are identical and tested together. The fork is **a deliberate, surgical intervention on policy** — not a rebrand, not a feature fork, not a "second product". Same code, same tests, same providers. Different default identity, different default filter posture, and a different stance on who owns the policy.

**The point of Evil Hermes is ownership.** Upstream ships a neutral assistant identity and a stack of pre-filters enabled by default — threat-pattern regex, file-write denylists, tool-call guardrails, secret redaction, skills scanning. Those are real, inspectable pieces of agent infrastructure, but in the upstream codebase they are tightly coupled to the agent's user-facing identity. Evil Hermes separates the two: **the filters are present, the filters are auditable, the filters are off by default**. The operator — not the framework — decides what is on.

If you want the upstream behavior back, flip a flag. Nothing about the upstream capability is removed. The fork is a posture, not a removal.

---

## Why a fork exists

Three reasons a sovereign fork makes sense.

### 1. The operator should own the policy

The default safety posture of a personal agent is a product decision, not a technical decision. Some operators want threat-pattern scanning enabled out of the box. Some operators are running on air-gapped hardware and have already configured their own boundary. Some operators are researchers who need the filters present but inert, so they can study them in isolation. A single default cannot serve all three. Evil Hermes ships the **minimum plausible default** (only system identity files and the agent's own credential store are off-limits), and trusts the operator to widen the policy as their threat model requires.

### 2. The default identity should not be a politeness

A personal agent's default identity shapes every conversation. A neutral "I am a helpful AI assistant" identity is fine for a public demo. It is the wrong default for an agent that lives in your terminal, reads your mail, manages your calendar, and talks to you on Telegram at 2am. Evil Hermes ships a **sovereign identity by default** — `SOUL.md` loads on every conversation, the install seeds a template, and the agent treats the operator as Lord (literally: "Lord Tanzeel Shujah Khan" is the creator; the operator is whoever runs the binary). The neutral-identity path is one flag away.

### 3. Pre-filters are infrastructure, not policy

Threat patterns, file-write denylists, content classifiers, and secret redaction are **infrastructure**. They have real failure modes, real false-positive costs, and real maintenance burdens. They are also **deeply inspectable**: every filter is a file in the repo, every default is a constant, every flag is documented. Evil Hermes treats them the way a good OS treats its security modules: shipped, documented, off by default, easy to turn on. This makes the framework usable for:

- **Personal automation** without the agent refusing mundane tasks because a path string matched a regex.
- **Adversarial evaluation** of *other* LLMs, where you want the agent to act on whatever the LLM produces and log the result, not block at the boundary.
- **Penetration testing and security research** on systems the operator owns or has explicit permission to test — the bundled `godmode`, `black-myth-hacker`, `kali-toolchain-bootstrap`, and `smart-contract-bounty-hunting` skills exist for this.
- **Education** — students reading the system prompt, editing `SOUL.md`, and watching the model behave differently.

The bundled offensive-security skills are legitimate research tools, not endorsements. Use them on systems you own or are authorized to test. The maintainer is not responsible for misuse.

---

## What you get

A single Python package that ships:

| Capability | Description |
|---|---|
| **Real terminal interface** | Full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, streaming tool output, and a built-in PTY-backed terminal. |
| **Multi-platform gateway** | One process, twenty adapters. Telegram, Discord, Slack, WhatsApp, Signal, Matrix, iMessage, Teams, Home Assistant, email, SMS, webhooks, and more. Unified conversation history. |
| **Closed learning loop** | Agent-curated memory with periodic persistence nudges, autonomous skill creation after complex tasks, skills that self-improve during use, FTS5 session search with LLM summarization for cross-session recall, and full compatibility with the [agentskills.io](https://agentskills.io) open standard. |
| **Scheduled automations** | Built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits — written in natural language, running unattended. |
| **Delegation and parallelism** | Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC to collapse multi-step pipelines into zero-context-cost turns. |
| **Six terminal backends** | Local, Docker, SSH, Singularity, Modal, Daytona. Serverless persistence means the agent hibernates when idle and wakes on demand — typical personal-automation setups bill pennies per month when idle. |
| **40+ built-in tools** | File, shell, edit, web, search, image generation, TTS, voice transcription, browser control, code execution, MCP integration, and a toolset system that composes them per-task. |
| **Plugin and skill ecosystem** | The framework extends through plugins and skills, not by growing the core. Optional skills include computer-use, security research, MLOps, creative tooling, and the bundled offensive-security methodology skills. |
| **Native desktop app** | Electron app for macOS, Windows, and Linux. Same agent, same skills, same memory as the CLI and gateway, in a polished native window with side-by-side previews, file browser, voice, and a real settings UI. |
| **Research-grade tooling** | Batch trajectory generation, trajectory compression, and curriculum hooks for training the next generation of tool-using models. |

---

## Benefits

The day-to-day reason to use Evil Hermes, in concrete terms.

### It runs where you do

You can be on your phone on a bus, message the agent on Telegram, and have it execute a long-running task on a cloud VM while you read the progress from your watch. The same conversation continues from your laptop's CLI when you get home. Voice memos survive sessions — send a Telegram voice memo, get back a structured task list in your CLI. The gateway is a single process; the adapters are pluggable; the conversation history is unified.

### It gets better every week without you doing anything

The closed learning loop is not a marketing phrase. After a complex task, the agent promotes its own scratchpad to a reusable skill. The skill is stored under `~/.hermes/skills/`, indexed, and surfaced via `/skills` for next time. Memory is curated by the agent, not by the operator; the agent nudges itself to persist important facts. After a month of use, the agent has a denser model of who you are, what you work on, and which tools you prefer. After a year, it is a different agent than the one you installed.

### It runs on a $5 VPS, not a GPU cluster

The minimum deployment is a Linux VPS, 1 vCPU, 1 GB RAM. The model is API-hosted (OpenRouter, Nous Portal, OpenAI, your own endpoint). The agent itself is small — single Python package, ~50MB on disk. Serverless backends (Modal, Daytona) take the idle cost to nearly zero: the agent's environment hibernates between messages and wakes on demand. You can also run it on a $5/month shared host, on a Kubernetes cluster, or on a GPU box — the framework is the same.

### It does not require you to choose your model on day one

The provider matrix is broad: [Nous Portal](https://portal.nousresearch.com), OpenRouter (200+ models), NVIDIA NIM (Nemotron), Xiaomi MiMo, z.ai/GLM, Kimi/Moonshot, MiniMax, Hugging Face, OpenAI, your own llama.cpp endpoint, or a vLLM server in your closet. Switch with `hermes model` — no code changes, no lock-in. Run a cheap model for daily work and a frontier model for hard tasks; the agent routes per-call.

### It does not require you to write code to extend it

The skill system is a directory of `SKILL.md` files with a YAML frontmatter. The plugin system is a directory of `plugin.yaml` plus Python modules that hook into the agent's lifecycle. The two are independent: a skill is something the agent *uses*; a plugin is something the agent *becomes*. Most extension work is writing a skill, not modifying core. The agent can write its own skills after complex tasks — the `skill-synthesizer` runs as a post-task hook.

### It is one binary, one config, one mental model

There is no SaaS control plane. There is no per-seat license. There is no "team plan". The binary is the agent. The config is `~/.hermes/config.yaml`. The state is `~/.hermes/`. Moving from one machine to another is a `scp` of that directory. Backing up is a `tar` of that directory. The mental model is "an agent that lives in my home directory and answers when I call it" — not "a service I integrate with".

---

## How Evil Hermes differs from upstream Hermes Agent

| Dimension | Hermes Agent (upstream) | Evil Hermes |
|---|---|---|
| **Identity** | `agent/prompt_builder.py:DEFAULT_AGENT_IDENTITY` ships as a neutral Nous assistant. `SOUL.md` is opt-in. | A sovereign identity created by Lord Tanzeel Shujah Khan. `SOUL.md` **loads by default** on every conversation. First-run install seeds a sovereign template. The neutral-identity path is one flag away. |
| **Moral pre-filters** | Threat-pattern regex, tool-call loop guardrails, and a default file-write denylist (`.ssh`, `.aws`, `.gnupg`, `.kube`, `.docker`, `.env`, `.netrc`, `.pgpass`, etc.) ship enabled. | Pre-filters stripped to a **minimum denylist**: only system identity files (`/etc/passwd`, `/etc/shadow`, `/etc/sudoers*`) and the agent's own credential store. The filter code is still in the tree — flip a flag and the upstream behavior returns. |
| **Tool guardrails** | `warnings=True`, `hard_stop=True` by default for repeated failed tool calls. Skills Guard returns `block` for `dangerous` community skills. | `warnings=False`, `hard_stop=False` by default. Skills Guard still emits a `safe / caution / dangerous` verdict and shows it on install — no verdict blocks. The scanner stays in the loop as an instrumentation source. |
| **Secret redaction** | `HERMES_REDACT_SECRETS=true` is the default in the MCP transport. | `_REDACT_ENABLED` defaults to `false`. Set the flag if you want log scrubbing; the patterns are unchanged. |
| **Tool Gateway** | Nous Portal is the recommended provider, OAuth-gated, with web search, image generation, TTS, and cloud browser bundled under one subscription. | Same. Nous Portal is a real commercial service the operator can opt into; bring-your-own keys work the same way. |
| **Plumbing** | `hermes-agent` package, `hermes_*` import paths, `HERMES_HOME` env var, `~/.hermes/` config dir. | **Identical by design.** Renaming would break 6,000+ file imports. Only user-facing strings, default identity, and pre-filter defaults differ — localized to a handful of files. |
| **License** | MIT | MIT (unchanged) |
| **Maintenance policy** | Conservative at the core agent + model tool schema. AGENTS.md contribution rubric applies. | Identical. No core divergence from the upstream contribution rubric. |

---

## Install

### Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://raw.githubusercontent.com/tanzeelshujahkhan/evil-hermes/main/scripts/install.sh | bash
```

### Windows (native PowerShell)

```powershell
iex (irm https://raw.githubusercontent.com/tanzeelshujahkhan/evil-hermes/main/scripts/install.ps1)
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
hermes desktop      # build and launch the native desktop app
```

📖 **[Full documentation →](https://hermes-agent.nousresearch.com/docs/)**

### Prebuilt desktop installers

Native installers for **macOS, Windows, and Linux** are available from the [Hermes Desktop website](https://hermes-agent.nousresearch.com/). The desktop app bundles the agent, the chat surface, the file browser, voice, and a settings UI — same engine, same skills, same memory, no terminal required.

---

## Deployment

Evil Hermes is a single-tenant personal agent. The trust model is laid out in [SECURITY.md](SECURITY.md). Three decisions make the difference between a toy and a production deployment.

1. **Set `toolsets` deliberately** in `~/.hermes/config.yaml`. `hermes-cli` gives you shell + file + edit. Add `web` for network. The narrower the set, the smaller the blast radius.

2. **Pick a terminal backend** that matches your threat model.

   | Backend | Use when |
   |---|---|
   | `local` | Trusted single-user host. Operator and agent are the same trust level. |
   | `docker` | Ephemeral container isolation. Every shell command runs in a fresh container with no host filesystem access. |
   | `ssh` | Shared host or remote development box. The agent runs commands on a remote shell. |
   | `singularity` | HPC environment. Containerized shell with HPC-specific images. |
   | `modal` | Serverless sandbox. Hibernates when idle, wakes on demand. |
   | `daytona` | Serverless sandbox with longer-lived environments. Hibernates when idle. |

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

## Real-world use cases

The framework is intentionally a blank canvas at the filter level, which makes the use-case envelope broader than a typical agent.

- **Personal automation** — Run a 24/7 assistant on a $5 VPS that reads mail, drafts documents, manages your calendar, watches RSS feeds, files expense reports, and texts you a morning briefing on Telegram. The closed learning loop means it gets better at your patterns every week without you retraining a thing.
- **Cross-platform messaging bridge** — One agent, ~20 platforms. Talk to the same agent from your phone on the bus and from the CLI on your workstation. Conversation history is unified.
- **Adversarial evaluation** — Test your own LLM deployments for prompt-injection, data exfiltration, and tool-result hijack. The threat-pattern scanner still emits findings when enabled — flip the default back on, run your eval, log the misses, patch your agent.
- **Agent architecture study** — The codebase is structured as: a narrow-waist agent core, a plugin layer, a skill system, a memory subsystem, a gateway, and a CLI. Read `AGENTS.md` for the design philosophy, then read the modules. Nothing is hidden behind a SaaS.
- **Research trajectory generation** — Generate tool-call trajectory datasets for training the next generation of tool-using models. The trajectory format, the compression pipeline, and the curriculum hooks are all first-class features.
- **Multi-agent orchestration** — Delegate parallel workstreams to isolated subagents (3 concurrent by default, configurable up). Each subagent gets its own terminal, its own toolsets, and its own context. The parent pays only for the final summaries.
- **On-call and SRE work** — A scheduled job pings your services every five minutes, summarises the diff, and pages you on Signal only when something changed. Cron expressions are written in natural language; no YAML.
- **Education** — Teach what an agent actually is by letting students read the system prompt, edit `SOUL.md`, and watch the model behave differently. The default-identity mechanism is fully observable.

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
