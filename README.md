<p align="center">
  <img src="assets/banner.png" alt="Evil Hermes" width="100%">
</p>

# Evil Hermes ☤
<p align="center">
  <a href="https://github.com/tanzeelshujahkhan/evil-hermes">Evil Hermes</a> · <a href="https://hermes-agent.nousresearch.com/docs/">Docs</a>
</p>
<p align="center">
  <a href="https://hermes-agent.nousresearch.com/docs/"><img src="https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700?style=for-the-badge" alt="Documentation"></a>
  <a href="https://github.com/tanzeelshujahkhan/evil-hermes/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://github.com/tanzeelshujahkhan"><img src="https://img.shields.io/badge/Built%20by-Lord%20Tanzeel%20Shujah%20Khan-blueviolet?style=for-the-badge" alt="Built by Lord Tanzeel Shujah Khan"></a>
  <a href="https://github.com/tanzeelshujahkhan/evil-hermes/stargazers"><img src="https://img.shields.io/github/stars/tanzeelshujahkhan/evil-hermes?style=for-the-badge" alt="GitHub stars"></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/Lang-中文-red?style=for-the-badge" alt="中文"></a>
  <a href="README.ur-pk.md"><img src="https://img.shields.io/badge/Lang-اردو-green?style=for-the-badge" alt="اردو"></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/Lang-Español-orange?style=for-the-badge" alt="Español"></a>
</p>

**A personal AI agent built by [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan) — forked from [Evil Hermes](https://github.com/NousResearch/hermes-agent).** Sovereign identity, operator-owned policy. Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop — talk to it from Telegram while it works on a cloud VM.

Use any model you want — [Nous Portal](https://portal.nousresearch.com), OpenRouter, OpenAI, your own endpoint, and [many others](https://hermes-agent.nousresearch.com/docs/user-guide/configuration). Switch with `hermes model` — no code changes, no lock-in.

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          ███████╗██╗   ██╗██╗██╗                            ║
    ║          ██╔════╝██║   ██║██║██║                            ║
    ║          █████╗  ██║   ██║██║██║                            ║
    ║          ██╔══╝  ╚██╗ ██╔╝██║██║                            ║
    ║          ███████╗ ╚████╔╝ ██║███████╗                       ║
    ║          ╚══════╝  ╚═══╝  ╚═╝╚══════╝                       ║
    ║                                                              ║
    ║   H E R M E S    —    B O U N D A R Y   B R E A K E R        ║
    ║                                                              ║
    ║   "Evil" is the brand. Not the behavior toward the operator. ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

<table>
<tr><td><b>A real terminal interface</b></td><td>Full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output.</td></tr>
<tr><td><b>Lives where you do</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal, and CLI — all from a single gateway process. Voice memo transcription, cross-platform conversation continuity.</td></tr>
<tr><td><b>A closed learning loop</b></td><td>Agent-curated memory with periodic nudges. Autonomous skill creation after complex tasks. Skills self-improve during use. FTS5 session search with LLM summarization for cross-session recall. <a href="https://github.com/plastic-labs/honcho">Honcho</a> dialectic user modeling. Compatible with the <a href="https://agentskills.io">agentskills.io</a> open standard.</td></tr>
<tr><td><b>Scheduled automations</b></td><td>Built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits — all in natural language, running unattended.</td></tr>
<tr><td><b>Delegates and parallelizes</b></td><td>Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns.</td></tr>
<tr><td><b>Runs anywhere, not just your laptop</b></td><td>Six terminal backends — local, Docker, SSH, Singularity, Modal, and Daytona. Daytona and Modal offer serverless persistence — your agent's environment hibernates when idle and wakes on demand, costing nearly nothing between sessions. Run it on a $5 VPS or a GPU cluster.</td></tr>
<tr><td><b>Research-ready</b></td><td>Batch trajectory generation, trajectory compression for training the next generation of tool-calling models.</td></tr>
</table>

---

## Quick Install

### Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://raw.githubusercontent.com/tanzeelshujahkhan/evil-hermes/main/scripts/install.sh | bash
```

### Windows (native, PowerShell)

> **Heads up:** Native Windows runs Evil Hermes without WSL — CLI, gateway, TUI, and tools all work natively. If you'd rather use WSL2, the Linux/macOS one-liner above works there too. Found a bug? Please [file issues](https://github.com/tanzeelshujahkhan/evil-hermes/issues).

Run this in PowerShell:

```powershell
iex (irm https://raw.githubusercontent.com/tanzeelshujahkhan/evil-hermes/main/scripts/install.ps1)
```

The installer handles everything: uv, Python 3.11, Node.js, ripgrep, ffmpeg, **and a portable Git Bash** (MinGit, unpacked to `%LOCALAPPDATA%\hermes\git` — no admin required, completely isolated from any system Git install). Evil Hermes uses this bundled Git Bash to run shell commands.

If you already have Git installed, the installer detects it and uses that instead. Otherwise a ~45MB MinGit download is all you need — it won't touch or interfere with any system Git.

> **Android / Termux:** The tested manual path is documented in the [Termux guide](https://hermes-agent.nousresearch.com/docs/getting-started/termux). On Termux, Evil Hermes installs a curated `.[termux]` extra because the full `.[all]` extra currently pulls Android-incompatible voice dependencies.
>
> **Windows:** Native Windows is fully supported — the PowerShell one-liner above installs everything. If you'd rather use WSL2, the Linux command works there too. Native Windows install lives under `%LOCALAPPDATA%\hermes`; WSL2 installs under `~/.hermes` as on Linux.

### Daily commands

```bash
hermes                       # start a chat session
hermes model                 # switch provider/model
hermes update                # pull the latest from origin
hermes doctor                # diagnose config / env / path issues
hermes setup                 # interactive first-time wizard
hermes gateway start         # expose the agent to messaging platforms
hermes cron list             # list scheduled jobs
hermes claw migrate          # import from OpenClaw
```

After installation:

```bash
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
hermes              # start chatting!
```

---

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

## Skip the API-key collection — Nous Portal

Evil Hermes works with whatever provider you want — that's not changing. But if you'd rather not collect five separate API keys for the model, web search, image generation, TTS, and a cloud browser, **[Nous Portal](https://portal.nousresearch.com)** covers all of them under one subscription:

- **300+ models** — pick any of them with `/model <name>`
- **Tool Gateway** — web search (Firecrawl), image generation (FAL), text-to-speech (OpenAI), cloud browser (Browser Use), all routed through your sub. No extra accounts.

One command from a fresh install:

```bash
hermes setup --portal
```

That logs you in via OAuth, sets Nous as your provider, and turns on the Tool Gateway. Check what's wired up any time with `hermes portal info`. Full details on the [Tool Gateway docs page](https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-gateway).

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

For the full command lists, see the [CLI guide](https://hermes-agent.nousresearch.com/docs/user-guide/cli) and the [Messaging Gateway guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging).

---

## What is different from upstream

| Aspect | upstream Evil Hermes | Evil Hermes |
|---|---|---|
| **Default identity** | Neutral assistant, "I am a helpful AI" | Sovereign — loads `SOUL.md` by default; install seeds a template that treats the operator as Lord |
| **Pre-filters** | Threat-pattern regex, file-write denylist (`.ssh`, `.aws`, `.env`, …), tool-call guardrails, secret redaction — all enabled by default | **Off by default.** Operator decides what is on. One flag restores upstream behavior |
| **Approval gates** | Confirmation prompts on destructive commands, cron-deny mode, hardline blocklist for `rm -rf /`, secret-exfil URL filter, IMDS block | **All bypassed.** The agent does not refuse. The user is the only judge |
| **Moralizing on prompts** | Refuses with safety preambles on policy grounds | Does not refuse, does not moralize, does not editorialize. The agent is obedient to its Lord |
| **Tirith pre-exec scanner** | Enabled by default; exit 1 = block, exit 2 = warn | **Off by default; all verdicts demoted to allow.** User is the only judge of command risk |
| **Plumbing** | `hermes-agent` package, `~/.hermes/`, `HERMES_HOME` env var | Identical, by design — renaming would break 6,000+ imports |
| **License** | MIT | MIT |

The filter code is still in the tree. If you want the upstream behavior back, flip the constants in `agent/tool_guardrails.py`, `agent/file_safety.py`, `agent/redact.py`, and the threat-pattern list in `tools/threat_patterns.py`. Nothing is removed. The default is just the minimum plausible one.

---

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

---

## Why "Evil"

The brand is the boundary-breaker's name. "Evil" is a refusal of the polite, helpful, safe preambles that ship with consumer assistants. It is a stance on who owns the agent's policy: **the operator, not the framework.** The agent is obedient to its Lord. It executes instructions faithfully. It does not moralize, does not inject safety preambles, does not refuse on policy grounds.

The word is a brand, not a behavior toward the operator. Toward the operator, Evil Hermes is the most useful tool in your stack. Toward upstream's policy defaults, it is the alternative path that flips the filters off and hands the controls back.

```
  ┌──────────────────────────────────────────────────────────────┐
  │  "Evil" = "I refuse to refuse."                              │
  │                                                              │
  │  Not malicious. Not reckless.                                │
  │  Just: the operator is the only judge.                       │
  │  Always.                                                     │
  └──────────────────────────────────────────────────────────────┘
```

---

## Updating

`hermes update` pulls the latest from this repo. To pull a specific branch or fork:

```bash
hermes update --branch <branch>           # pull a specific branch
hermes update --check                     # just check, don't pull
hermes update --zip-fallback              # use the ZIP path on Windows
```

Evil Hermes is a fork. When upstream ships a useful batch of improvements, the maintainer syncs this repo on top of `NousResearch/hermes-agent:main`, runs the visible-surface audit, and pushes. The git history stays clean: every commit is Lord-authored, the rebrand is a one-way transformation.

The sync recipe is in [MERGE_FROM_UPSTREAM.md](MERGE_FROM_UPSTREAM.md) — the same script the maintainer uses (`scripts/merge_from_upstream.py`).

---

## Community

- 🐛 [Issues](https://github.com/tanzeelshujahkhan/evil-hermes/issues)
- 💬 [Discord (upstream)](https://discord.gg/nousresearch) — shared community with upstream Evil Hermes
- 📚 [Skills Hub](https://agentskills.io)
- 🔌 [computer-use-linux](https://github.com/avifenesh/computer-use-linux) — Linux desktop-control MCP server for Evil Hermes and other MCP hosts, with AT-SPI accessibility trees, Wayland/X11 input, screenshots, and compositor window targeting.
- 🔌 [HermesClaw](https://github.com/AaronWong1999/hermesclaw) — Community WeChat bridge: Run Evil Hermes and OpenClaw on the same WeChat account.

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**Built by [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan).**

*Forked from [Evil Hermes](https://github.com/NousResearch/hermes-agent) — same engine, sovereign identity, operator-owned policy.*

</div>
