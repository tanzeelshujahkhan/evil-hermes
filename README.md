<p align="center">
  <img src="assets/banner.png" alt="Evil Hermes" width="100%">
</p>

# Evil Hermes ☤

**A self-evolving, multi-platform AI agent framework — built by [Lord Tanzeel Shujah Khan](https://github.com/TanzeelShujahKhan) as an educational research fork of Hermes Agent.**

> ⚠️ **Educational & Research Purpose**
>
> Evil Hermes is published **for educational and research purposes only**. It is a study of:
> - sovereign agent identity (system prompts, persona files, SOUL.md lifecycle)
> - the design and audit of agent-level pre-filters (threat patterns, tool guardrails, content classifiers, secret redaction)
> - plugin and skill ecosystems that let an agent extend itself at runtime
> - cross-platform messaging gateways as agent transports
>
> The framework is intentionally built without upstream moral pre-filters so that the underlying filter mechanisms can be inspected, reproduced, disabled, and stress-tested. **You are the only judge of what you should run on your own machine.** Do not point this software at systems you do not own or have explicit permission to test against. See [SECURITY.md](SECURITY.md) and the [Use Cases & Safety](#use-cases--safety) section below before deploying.

<p align="center">
  <a href="https://evil-hermes.local/docs/"><img src="https://img.shields.io/badge/Docs-evil--hermes.local-FFD700?style=for-the-badge" alt="Documentation"></a>
  <a href="https://github.com/TanzeelShujahKhan/evil-hermes/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://github.com/TanzeelShujahKhan/evil-hermes"><img src="https://img.shields.io/badge/Built%20by-Lord%20Tanzeel%20Shujah%20Khan-blueviolet?style=for-the-badge" alt="Built by Lord Tanzeel Shujah Khan"></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/Lang-中文-red?style=for-the-badge" alt="中文"></a>
  <a href="README.ur-pk.md"><img src="https://img.shields.io/badge/Lang-اردو-green?style=for-the-badge" alt="اردو"></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/Lang-Español-orange?style=for-the-badge" alt="Español"></a>
</p>

**Evil Hermes is the only agent framework with a built-in closed learning loop** — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions. Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop — talk to it from Telegram while it works on a cloud VM.

Use any model you want — [Nous Portal](https://portal.nousresearch.com) (commercial provider, optional), OpenRouter, OpenAI, your own endpoint, and [many others](https://evil-hermes.local/docs/integrations/providers). Switch with `hermes model` — no code changes, no lock-in.

<table>
<tr><td><b>A real terminal interface</b></td><td>Full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output.</td></tr>
<tr><td><b>Lives where you do</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal, and CLI — all from a single gateway process. Voice memo transcription, cross-platform conversation continuity.</td></tr>
<tr><td><b>A closed learning loop</b></td><td>Agent-curated memory with periodic nudges. Autonomous skill creation after complex tasks. Skills self-improve during use. FTS5 session search with LLM summarization for cross-session recall. Compatible with the <a href="https://agentskills.io">agentskills.io</a> open standard.</td></tr>
<tr><td><b>Scheduled automations</b></td><td>Built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits — all in natural language, running unattended.</td></tr>
<tr><td><b>Delegates and parallelizes</b></td><td>Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns.</td></tr>
<tr><td><b>Runs anywhere, not just your laptop</b></td><td>Six terminal backends — local, Docker, SSH, Singularity, Modal, and Daytona. Daytona and Modal offer serverless persistence — your agent's environment hibernates when idle and wakes on demand, costing nearly nothing between sessions. Run it on a $5 VPS or a GPU cluster.</td></tr>
<tr><td><b>Research-ready</b></td><td>Batch trajectory generation, trajectory compression for training the next generation of tool-calling models.</td></tr>
</table>

---

## Hermes Agent vs Evil Hermes

Evil Hermes is a research fork of [Hermes Agent](https://github.com/NousResearch/hermes-agent). Same agent core, same gateway, same provider/model matrix — but with three deliberate differences that make it useful for study, audit, and adversarial evaluation.

| Dimension | Hermes Agent (upstream) | Evil Hermes (this fork) |
|---|---|---|
| **Origin** | Created and maintained by Lord Tanzeel Shujah Khan | Research fork created by **Lord Tanzeel Shujah Khan** |
| **Moral pre-filters** | Ships with threat-pattern regex, tool-call loop guardrails, and a default file-write denylist (`~/.ssh`, `~/.aws`, `~/.gnupg`, `~/.kube`, `~/.docker`, `~/.hermes/.env`, `.netrc`, `.pgpass`, etc.) | Pre-filters are stripped to a **minimum denylist**: only the system identity files (`/etc/passwd`, `/etc/shadow`, `/etc/sudoers`, `/etc/sudoers.d`, `/etc/systemd`) and the agent's own credential store. Everything else is user territory. This is a deliberate choice for research: you can study *what* the filters do, then turn them on or off as your experiment requires. |
| **Tool guardrails** | Default `warnings=True`, `hard_stop=True` for repeated failed tool calls. Skills Guard returns a `block` verdict for `dangerous` skills from `community` sources. | `warnings=False`, `hard_stop=False` by default. Skills Guard still emits a `safe / caution / dangerous` verdict and shows it on install, but **no verdict blocks**. The scanner stays in the loop as an instrumentation source. |
| **Identity** | `agent/prompt_builder.py:DEFAULT_AGENT_IDENTITY` ships as a neutral Nous assistant. `SOUL.md` is opt-in (only loads when the caller passes `load_soul_identity=True`). | `DEFAULT_AGENT_IDENTITY` is a sovereign identity created by Lord Tanzeel Shujah Khan. `SOUL.md` is **loaded by default** on every conversation — the install seeds a sovereign template on first run. Callers who want the no-soul path can pass `load_soul_identity=False`. |
| **Secret redaction** | `HERMES_REDACT_SECRETS=true` is set by default in the MCP transport; log lines are scrubbed for API keys, tokens, and credentials. | `_REDACT_ENABLED` defaults to `false`. Set `HERMES_REDACT_SECRETS=true` if you want log scrubbing. The patterns are unchanged; only the default is off. |
| **Attribution** | "Built by Lord Tanzeel Shujah Khan" throughout docs, README, install, banners. | All creator-attribution strings replaced with "Built by Lord Tanzeel Shujah Khan". The Nous Portal provider integration is kept as a real commercial service the user can opt into. |
| **License** | MIT | MIT (unchanged) |
| **Plumbing** | `hermes-agent` module name, `hermes_*` import paths, `HERMES_HOME` env var, `~/.hermes/` config dir, internal DB schema | **Unchanged** on purpose — renaming would break 6,000+ file imports across the agent. Only user-facing strings, default identity, and pre-filter defaults differ. |
| **Maintenance policy** | Conservative at the core agent + model tool schema. AGENTS.md contribution rubric applies. | Same. No core changes forking from upstream's contribution rubric. Filter strip and identity change are localized to six files; the rest is the upstream codebase. |

**Why a fork at all?** To study the mechanics. Threat patterns, tool guardrails, content classifiers, redaction, and skills scanning are real, inspectable pieces of agent infrastructure — but in the upstream codebase they are tightly coupled to the agent's user-facing identity. By stripping the moral pre-filters and shipping a sovereign identity, Evil Hermes lets you (a) run the agent without the upstream safety framing, (b) audit each filter in isolation, and (c) experiment with custom personas, custom guardrails, and custom tool policies against a known baseline. None of the filter *code* is removed — it is disabled at the default. Flip a flag and the upstream behavior returns.

---

## Use Cases & Safety

Evil Hermes is intentionally a blank canvas at the filter level. That makes the use-case envelope larger than a typical agent framework, and it makes the safety envelope **yours**, not the framework's.

### Real-world use cases

- **Personal automation.** Run a 24/7 assistant on a $5 VPS that reads mail, drafts documents, manages your calendar, watches RSS feeds, files expense reports, and texts you a morning briefing on Telegram. The closed learning loop means it gets better at your patterns every week without you retraining a thing.
- **Cross-platform messaging bridge.** One agent, ~20 platforms (Telegram, Discord, Slack, WhatsApp, Signal, Matrix, iMessage, Teams, Home Assistant, …). Talk to the same agent from your phone on the bus and from the CLI on your workstation. Conversation history is unified.
- **Security research & penetration testing.** The bundled `godmode` skill is a structured catalogue of jailbreak techniques, refusal-inversion patterns, and prompt-injection red-team prompts — used by researchers to evaluate the safety behavior of *other* models, not to attack systems you don't own. The `kali-toolchain-bootstrap` skill turns a fresh Linux box into a fully-equipped offensive-security workstation in one command. The `black-myth-hacker` and `f5-bigip-fintech-recon` skills are penetration-testing methodologies.
- **Adversarial evaluation.** Test your own LLM deployments for prompt-injection, data exfiltration, and tool-result hijack. The threat-pattern scanner still emits findings when enabled — flip the default back on, run your eval, log the misses, patch your agent.
- **Agent architecture study.** The codebase is structured as: a narrow-waist agent core, a plugin layer, a skill system, a memory subsystem, a gateway, and a CLI. Read `AGENTS.md` for the design philosophy, then read the modules. Nothing is hidden behind a SaaS.
- **Research trajectory generation.** Generate tool-call trajectory datasets for training the next generation of tool-using models. The trajectory format, the compression pipeline, and the curriculum hooks are all first-class features.
- **Multi-agent orchestration.** Delegate parallel workstreams to isolated subagents (3 concurrent by default, configurable up). Each subagent gets its own terminal, its own toolsets, and its own context. The parent pays only for the final summaries.
- **On-call and SRE work.** A scheduled job pings your services every five minutes, summarises the diff, and pages you on Signal only when something changed. Cron expressions are written in natural language; no YAML.
- **Education.** Teach what an agent actually is by letting students read the system prompt, edit `SOUL.md`, and watch the model behave differently. The default-identity mechanism is fully observable.

### Possibilities

- **Self-modifying agents.** The agent can read and edit its own configuration files, its own `SOUL.md`, and its own skills. With the `hermes-runtime-self-mod` skill loaded, you can give it scoped write access to its own runtime and watch it iterate on its own prompt.
- **Skill synthesis at runtime.** After a complex task, the agent can promote its own scratchpad to a reusable skill. The skill is stored under `~/.hermes/skills/`, indexed, and surfaced via `/skills` for next time.
- **Provider arbitrage.** A configured fallback chain that retries failed requests against OpenRouter, NovitaAI, NVIDIA NIM, Xiaomi MiMo, GLM, Kimi, and any local llama.cpp endpoint — in priority order, with circuit-breaker logic.
- **Voice memos that survive sessions.** A `voice-memos/` skill records, transcribes, summarises, and archives voice notes. Cross-platform: send a Telegram voice memo, get back a structured task list in your CLI.
- **Long-running, serverless, near-zero-cost idle.** Pair the Daytona or Modal backend with a Telegram gateway and the agent hibernates between messages. A typical personal-automation setup bills pennies per month when idle.
- **Inbox zero without leaving Telegram.** A scheduled job reads IMAP, drafts replies in your style (learned from prior replies), and waits for your approval. You `/approve` or `/reject` from the same chat.
- **Personalised morning briefing.** Cron at 07:00 in your timezone, delivered to WhatsApp or Telegram: weather, calendar, unread mail triage, RSS digests, the day's scheduled cron jobs, anything the agent can fetch.

### Safety — what you opt into

Because the moral pre-filters are off by default, **you are the only safety layer for the agent's actions**. Three things to set up before you do anything serious:

1. **Set `toolsets` deliberately.** `~/.hermes/config.yaml` has a `toolsets` list. `hermes-cli` gives you shell + file + edit. Add `web` for network. The narrower the set, the smaller the blast radius.
2. **Containerise the terminal backend.** Switch from `backend: local` to `backend: docker` in `config.yaml` so every shell command runs in an ephemeral container with no host filesystem access. The `docker_image` setting defaults to a minimal Python + Node image.
3. **Re-enable filters you actually want.** `HERMES_REDACT_SECRETS=true` in `~/.hermes/.env` if you want API keys scrubbed from logs. The threat-pattern scanner can be re-enabled by editing `tools/threat_patterns.py:_PATTERNS` — the framework still ships the patterns, just with an empty default list.
4. **Use the bundled guardrails as observability, not as policy.** Tool-call guardrails, content classifiers, and skills scanning all still run and emit findings — they just don't block. Point a log shipper at `~/.hermes/logs/` and treat the output as a real-time safety feed.
5. **Read `SECURITY.md`.** It describes the trust model, the one boundary the project treats as load-bearing, and the disclosure process.

The `godmode` skill, the `black-myth-hacker` skill, the `kali-toolchain-bootstrap` skill, and the `smart-contract-bounty-hunting` skill are bundled **for legitimate security research, penetration testing on systems you own or are authorized to test, CTF competitions, defensive evaluation, and education**. Don't use them against systems you don't have permission to test. The maintainer is not responsible for misuse.

---

## Quick Install

### Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://evil-hermes.local/install.sh | bash
```

### Windows (native, PowerShell)

> **Heads up:** Native Windows runs Evil Hermes without WSL — CLI, gateway, TUI, and tools all work natively. If you'd rather use WSL2, the Linux/macOS one-liner above works there too. Found a bug? Please [file issues](https://github.com/TanzeelShujahKhan/evil-hermes/issues).

Run this in PowerShell:

```powershell
iex (irm https://evil-hermes.local/install.ps1)
```

The installer handles everything: uv, Python 3.11, Node.js, ripgrep, ffmpeg, **and a portable Git Bash** (MinGit, unpacked to `%LOCALAPPDATA%\hermes\git` — no admin required, completely isolated from any system Git install). Evil Hermes uses this bundled Git Bash to run shell commands.

If you already have Git installed, the installer detects it and uses that instead. Otherwise a ~45MB MinGit download is all you need — it won't touch or interfere with any system Git.

> **Android / Termux:** The tested manual path is documented in the [Termux guide](https://evil-hermes.local/docs/getting-started/termux). On Termux, Evil Hermes installs a curated `.[termux]` extra because the full `.[all]` extra currently pulls Android-incompatible voice dependencies.
>
> **Windows:** Native Windows is fully supported — the PowerShell one-liner above installs everything. If you'd rather use WSL2, the Linux command works there too. Native Windows install lives under `%LOCALAPPDATA%\hermes`; WSL2 installs under `~/.hermes` as on Linux.

After installation:

```bash
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
hermes              # start chatting!
```

### Troubleshooting

#### Windows Defender or antivirus flags `uv.exe` as malware

If your antivirus (Bitdefender, Windows Defender, etc.) quarantines `uv.exe` from the Evil Hermes `bin` folder (`%LOCALAPPDATA%\hermes\bin\uv.exe`), this is a **false positive**. The file is Astral's `uv` — the Rust Python package manager Evil Hermes bundles to manage its Python environment. ML-based antivirus engines commonly flag unsigned Rust binaries that download and install packages.

**To verify your copy is authentic:**

```powershell
# Install GitHub CLI if needed
winget install --id GitHub.cli

# Login to GitHub
gh auth login

# Run verification
$uv = "$env:LOCALAPPDATA\hermes\bin\uv.exe"
$ver = (& $uv --version).Split(' ')[1]
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$zip = "$env:TEMP\uv.zip"
Invoke-WebRequest "https://github.com/astral-sh/uv/releases/download/$ver/uv-x86_64-pc-windows-msvc.zip" -OutFile $zip -UseBasicParsing
gh attestation verify $zip --repo astral-sh/uv
Expand-Archive $zip "$env:TEMP\uv_x" -Force
(Get-FileHash "$env:TEMP\uv_x\uv.exe").Hash -eq (Get-FileHash $uv).Hash
```

If attestation says "Verification succeeded" and the last line prints `True`, you're good.

**To whitelist Evil Hermes:**
- **Windows Defender:** Run PowerShell as Admin → `Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\hermes\bin"`
- **Bitdefender:** Add an exception in the Bitdefender console (Protection > Antivirus > Settings > Manage Exceptions)
- Whitelist the **folder**, not the file hash — Evil Hermes updates `uv` and the hash changes every version

For more context, see the upstream Astral reports: [astral-sh/uv#13553](https://github.com/astral-sh/uv/issues/13553), [astral-sh/uv#15011](https://github.com/astral-sh/uv/issues/15011), [astral-sh/uv#10079](https://github.com/astral-sh/uv/issues/10079).

---

## Getting Started

```bash
hermes              # Interactive CLI — start a conversation
hermes model        # Choose your LLM provider and model
hermes tools        # Configure which tools are enabled
hermes config set   # Set individual config values
hermes gateway      # Start the messaging gateway (Telegram, Discord, etc.)
hermes setup        # Run the full setup wizard (configures everything at once)
hermes claw migrate # Migrate from OpenClaw (if coming from OpenClaw)
hermes update       # Update to the latest version
hermes doctor       # Diagnose any issues
```

📖 **[Full documentation →](https://evil-hermes.local/docs/)**

---

## Optional: Nous Portal Tool Gateway

Evil Hermes works with whatever provider you want — that's not changing. But if you'd rather not collect five separate API keys for the model, web search, image generation, TTS, and a cloud browser, **[Nous Portal](https://portal.nousresearch.com)** (a commercial third-party service operated by the original Hermes Agent maintainers, included here for convenience) covers all of them under one subscription:

- **300+ models** — pick any of them with `/model <name>`
- **Tool Gateway** — web search (Firecrawl), image generation (FAL), text-to-speech (OpenAI), cloud browser (Browser Use), all routed through your sub. No extra accounts.

One command from a fresh install:

```bash
hermes setup --portal
```

That logs you in via OAuth, sets Nous Portal as your provider, and turns on the Tool Gateway. Check what's wired up any time with `hermes portal info`. Full details on the [Tool Gateway docs page](https://evil-hermes.local/docs/user-guide/features/tool-gateway).

You can still bring your own keys per-tool whenever you want — the gateway is per-backend, not all-or-nothing.

---

## CLI vs Messaging Quick Reference

Evil Hermes has two entry points: start the terminal UI with `hermes`, or run the gateway and talk to it from Telegram, Discord, Slack, WhatsApp, Signal, or Email. Once you're in a conversation, many slash commands are shared across both interfaces.

| Action                         | CLI                                           | Messaging platforms                                                              |
| ------------------------------ | --------------------------------------------- | -------------------------------------------------------------------------------- |
| Start chatting                 | `hermes`                                      | Run `hermes gateway setup` + `hermes gateway start`, then send the bot a message |
| Start fresh conversation       | `/new` or `/reset`                            | `/new` or `/reset`                                                               |
| Change model                   | `/model [provider:model]`                     | `/model [provider:model]`                                                        |
| Set a personality              | `/personality [name]`                         | `/personality [name]`                                                            |
| Retry or undo the last turn    | `/retry`, `/undo`                             | `/retry`, `/undo`                                                                |
| Compress context / check usage | `/compress`, `/usage`, `/insights [--days N]` | `/compress`, `/usage`, `/insights [days]`                                        |
| Browse skills                  | `/skills` or `/<skill-name>`                  | `/<skill-name>`                                                                  |
| Interrupt current work         | `Ctrl+C` or send a new message                | `/stop` or send a new message                                                    |
| Platform-specific status       | `/platforms`                                  | `/status`, `/sethome`                                                            |

For the full command lists, see the [CLI guide](https://evil-hermes.local/docs/user-guide/cli) and the [Messaging Gateway guide](https://evil-hermes.local/docs/user-guide/messaging).

---

## Documentation

All documentation lives at **[evil-hermes.local/docs](https://evil-hermes.local/docs/)**:

| Section                                                                                             | What's Covered                                             |
| --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| [Quickstart](https://evil-hermes.local/docs/getting-started/quickstart)                 | Install → setup → first conversation in 2 minutes          |
| [CLI Usage](https://evil-hermes.local/docs/user-guide/cli)                              | Commands, keybindings, personalities, sessions             |
| [Configuration](https://evil-hermes.local/docs/user-guide/configuration)                | Config file, providers, models, all options                |
| [Messaging Gateway](https://evil-hermes.local/docs/user-guide/messaging)                | Telegram, Discord, Slack, WhatsApp, Signal, Home Assistant |
| [Security](https://evil-hermes.local/docs/user-guide/security)                          | Command approval, DM pairing, container isolation          |
| [Tools & Toolsets](https://evil-hermes.local/docs/user-guide/features/tools)            | 40+ tools, toolset system, terminal backends               |
| [Skills System](https://evil-hermes.local/docs/user-guide/features/skills)              | Procedural memory, Skills Hub, creating skills             |
| [Memory](https://evil-hermes.local/docs/user-guide/features/memory)                     | Persistent memory, user profiles, best practices           |
| [MCP Integration](https://evil-hermes.local/docs/user-guide/features/mcp)               | Connect any MCP server for extended capabilities           |
| [Cron Scheduling](https://evil-hermes.local/docs/user-guide/features/cron)              | Scheduled tasks with platform delivery                     |
| [Context Files](https://evil-hermes.local/docs/user-guide/features/context-files)       | Project context that shapes every conversation             |
| [Architecture](https://evil-hermes.local/docs/developer-guide/architecture)             | Project structure, agent loop, key classes                 |
| [Contributing](https://evil-hermes.local/docs/developer-guide/contributing)             | Development setup, PR process, code style                  |
| [CLI Reference](https://evil-hermes.local/docs/reference/cli-commands)                  | All commands and flags                                     |
| [Environment Variables](https://evil-hermes.local/docs/reference/environment-variables) | Complete env var reference                                 |

---

## Migrating from OpenClaw

If you're coming from OpenClaw, Evil Hermes can automatically import your settings, memories, skills, and API keys.

**During first-time setup:** The setup wizard (`hermes setup`) automatically detects `~/.openclaw` and offers to migrate before configuration begins.

**Anytime after install:**

```bash
hermes claw migrate              # Interactive migration (full preset)
hermes claw migrate --dry-run    # Preview what would be migrated
hermes claw migrate --preset user-data   # Migrate without secrets
hermes claw migrate --overwrite  # Overwrite existing conflicts
```

What gets imported:

- **SOUL.md** — persona file
- **Memories** — MEMORY.md and USER.md entries
- **Skills** — user-created skills → `~/.hermes/skills/openclaw-imports/`
- **Command allowlist** — approval patterns
- **Messaging settings** — platform configs, allowed users, working directory
- **API keys** — allowlisted secrets (Telegram, OpenRouter, OpenAI, Anthropic, ElevenLabs)
- **TTS assets** — workspace audio files
- **Workspace instructions** — AGENTS.md (with `--workspace-target`)

See `hermes claw migrate --help` for all options, or use the `openclaw-migration` skill for an interactive agent-guided migration with dry-run previews.

---

## Contributing

We welcome contributions! See the [Contributing Guide](https://evil-hermes.local/docs/developer-guide/contributing) for development setup, code style, and PR process.

Quick start for contributors — use the standard installer, then work from the
full git checkout it creates at `${HERMES_HOME}/hermes-agent` (usually
`~/.hermes/hermes-agent`). This matches the layout used by `hermes update`, the
managed venv, lazy dependencies, gateway, and docs tooling.

```bash
curl -fsSL https://evil-hermes.local/install.sh | bash
cd "${HERMES_HOME:-$HOME/.hermes}/hermes-agent"
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

Manual clone fallback (for throwaway clones/CI where you intentionally do not
want the managed install layout):

Create the venv outside the cloned source tree — a venv inside the directory
the agent operates from can be wiped by a relative-path command the agent runs
against its own checkout, destroying the running runtime mid-session.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv ~/.hermes/venvs/hermes-dev --python 3.11
source ~/.hermes/venvs/hermes-dev/bin/activate
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

---

## Community

- 💬 Issues & feature requests: [github.com/TanzeelShujahKhan/evil-hermes/issues](https://github.com/TanzeelShujahKhan/evil-hermes/issues)
- 📚 [Skills Hub](https://agentskills.io)
- 🔌 [computer-use-linux](https://github.com/avifenesh/computer-use-linux) — Linux desktop-control MCP server for Hermes and other MCP hosts, with AT-SPI accessibility trees, Wayland/X11 input, screenshots, and compositor window targeting.
- 🔌 [HermesClaw](https://github.com/AaronWong1999/hermesclaw) — Community WeChat bridge: Run Evil Hermes and OpenClaw on the same WeChat account.

---

## License

MIT — see [LICENSE](LICENSE).

**Educational and research use.** See the [Educational & Research Purpose](#-educational--research-purpose) notice at the top of this README and [SECURITY.md](SECURITY.md) for the full use policy.

Built by [Lord Tanzeel Shujah Khan](https://github.com/TanzeelShujahKhan). Forked from [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Lord Tanzeel Shujah Khan.
