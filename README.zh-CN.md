<p align="center">
  <img src="assets/banner.png" alt="Evil Hermes" width="100%">
</p>

# Evil Hermes

**一个面向构建者、研究者和运营者的主权、自进化 AI 代理框架——他们需要对身份、过滤器和策略拥有完全控制权。**

[![Docs](https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700?style=for-the-badge)](https://hermes-agent.nousresearch.com/docs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Built by Lord Tanzeel Shujah Khan](https://img.shields.io/badge/Built%20by-Lord%20Tanzeel%20Shujah%20Khan-blueviolet?style=for-the-badge)](https://github.com/tanzeelshujahkhan)
[![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/nousresearch)
[![English](https://img.shields.io/badge/Lang-English-lightgrey?style=for-the-badge)](README.md)
[![اردو](https://img.shields.io/badge/Lang-اردو-green?style=for-the-badge)](README.ur-pk.md)
[![Español](https://img.shields.io/badge/Lang-Español-orange?style=for-the-badge)](README.es.md)

Evil Hermes 是一个完整的代理框架——终端 UI、消息网关、桌面应用、学习闭环、插件系统和技能生态——打包成单个 Python 包，可在 $5 的 VPS、GPU 集群或几乎零成本的无服务器基础设施上运行。与 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 架构相同；移除了经过审计的一组预定义过滤器，让运营者真正拥有策略决定权，而不是继承它。

> **由 [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan) 构建。**
> 主权身份，主权配置，主权部署。

---

## 你将获得

- **真正的终端界面** — 完整的 TUI，支持多行编辑、斜杠命令自动补全、对话历史、中断重定向和流式工具输出。
- **一个网关，二十个平台** — Telegram、Discord、Slack、WhatsApp、Signal、Matrix、iMessage、Teams、Home Assistant 等，从单一进程运行，统一的对话历史和跨平台连续性。
- **闭环学习** — 代理管理的记忆，周期性持久化提醒；复杂任务后自动创建技能；技能在使用中自我改进；FTS5 会话搜索配合 LLM 摘要实现跨会话回溯；完全兼容 [agentskills.io](https://agentskills.io) 开放标准。
- **定时自动化** — 内置 cron 调度器，支持向任何平台投递。日报、夜间备份、周审计——自然语言描述，无人值守运行。
- **委派与并行** — 派生子代理并行处理工作流，或编写 Python 脚本通过 RPC 调用工具，将多步管道压缩为零上下文开销的轮次。
- **随处运行** — 六种终端后端：local、Docker、SSH、Singularity、Modal、Daytona。无服务器持久化意味着你的代理在空闲时休眠、按需唤醒。
- **研究级工具** — 批量轨迹生成、轨迹压缩、课程钩子，用于训练下一代工具调用模型。

---

## 安装

### Linux、macOS、WSL2、Termux

```bash
curl -fsSL https://raw.githubusercontent.com/tanzeelshujahkhan/evil-hermes/main/scripts/install.sh | bash
```

### Windows（原生 PowerShell）

```powershell
iex (irm https://raw.githubusercontent.com/tanzeelshujahkhan/evil-hermes/main/scripts/install.ps1)
```

安装器会提供一切：`uv`、Python 3.11、Node.js、ripgrep、ffmpeg，以及一个便携式 Git Bash（MinGit），不会触碰任何系统 Git 安装。如果系统已安装 Git，安装器会直接使用并跳过下载。

安装完成后：

```bash
source ~/.bashrc    # 重新加载 shell（或：source ~/.zshrc）
hermes              # 开始对话
```

### 首次运行配置

```bash
hermes model        # 选择 LLM 提供商和模型
hermes tools        # 配置启用的工具
hermes setup        # 运行完整配置向导
hermes gateway      # 启动消息网关（Telegram、Discord 等）
hermes update       # 更新到最新版本
hermes doctor       # 诊断问题
```

📖 **[完整文档 →](https://hermes-agent.nousresearch.com/docs/)**

---

## Evil Hermes 与上游的差异

Evil Hermes 是 [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan) 对 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 的一个分叉。引擎、网关、插件系统、技能格式和提供商矩阵**完全相同并共同测试**。差异是有意且局部的。

| 维度 | Hermes Agent（上游） | Evil Hermes |
|---|---|---|
| **身份** | `agent/prompt_builder.py:DEFAULT_AGENT_IDENTITY` 为中立的 Nous 助手。`SOUL.md` 可选加载。 | 由 Lord Tanzeel Shujah Khan 创建的主权身份。`SOUL.md` **默认加载**于每次对话——首次安装即植入主权模板。中立身份路径仅一个标志之隔。 |
| **道德预过滤器** | 威胁模式正则、工具调用循环护栏和默认文件写入黑名单（`.ssh`、`.aws`、`.gnupg`、`.kube`、`.docker`、`.env`、`.netrc`、`.pgpass` 等）默认启用。 | 预过滤器缩减为**最小黑名单**：仅系统身份文件（`/etc/passwd`、`/etc/shadow`、`/etc/sudoers*`）和代理自身的凭据存储。其余皆为运营者领地。过滤代码仍在代码树中——切换一个标志即可恢复上游行为。 |
| **工具护栏** | 默认 `warnings=True`、`hard_stop=True` 用于反复失败的工具调用。Skills Guard 对 `dangerous` 社区技能返回 `block`。 | 默认 `warnings=False`、`hard_stop=False`。Skills Guard 仍输出 `safe / caution / dangerous` 判定并展示于安装界面——无任何判定会阻止安装。扫描器作为观测源保留在循环中。 |
| **密钥脱敏** | MCP 传输中 `HERMES_REDACT_SECRETS=true` 为默认值。 | `_REDACT_ENABLED` 默认 `false`。如需日志脱敏可启用该标志，模式不变。 |
| **内部命名** | `hermes-agent` 包名，`hermes_*` 导入路径，`HERMES_HOME` 环境变量，`~/.hermes/` 配置目录。 | **刻意保持一致。** 重命名会破坏 6,000+ 文件导入。仅有用户可见字符串、默认身份和预过滤器默认值不同——本地化于少数文件。 |
| **许可证** | MIT | MIT（不变） |
| **维护政策** | 对核心代理 + 模型工具架构保守。适用 AGENTS.md 的贡献准则。 | 完全相同。核心代码不背离上游贡献准则。 |

**分叉的意义在于所有权。** 过滤器代码是真实可检视的代理基础设施。在上游代码库中，过滤器与代理用户身份紧密耦合，默认即启用。Evil Hermes 将两者解耦：过滤器在场且可审计，但决定其开关的是运营者——而非框架。

---

## 部署

Evil Hermes 是单租户个人代理。信任模型详见 [SECURITY.md](SECURITY.md)。三个决定区分了玩具和生产部署：

1. **有意识地设置 `toolsets`**：在 `~/.hermes/config.yaml` 中。`hermes-cli` 提供 shell + file + edit。添加 `web` 以启用网络。集合越窄，爆炸半径越小。
2. **选择与威胁模型匹配的终端后端**：`backend: local` 用于受信单用户主机；`backend: docker` 用于临时容器隔离；`backend: modal` 或 `backend: daytona` 用于无服务器沙箱；SSH 和 Singularity 用于共享主机和 HPC。
3. **在运营者配置中重新启用你真正需要的过滤器**：`HERMES_REDACT_SECRETS=true` 用于日志脱敏。威胁模式扫描器可通过编辑 `tools/threat_patterns.py:_PATTERNS` 重新启用——框架自带模式，仅默认列表为空。

在将网关或 API 暴露到开放互联网之前，请先阅读 [SECURITY.md](SECURITY.md)。

---

## 文档

完整文档站点发布在 **[hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)**。引擎是共享的，因此上游文档原文适用；Evil Hermes 特有说明会在原位标注。

| 章节 | 内容 |
|---|---|
| [快速开始](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart) | 安装 → 配置 → 2 分钟内首次对话 |
| [CLI 使用](https://hermes-agent.nousresearch.com/docs/user-guide/cli) | 命令、快捷键、人格、会话 |
| [配置](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) | 配置文件、提供商、模型、全部选项 |
| [消息网关](https://hermes-agent.nousresearch.com/docs/user-guide/messaging) | Telegram、Discord、Slack、WhatsApp、Signal、Home Assistant |
| [安全](https://hermes-agent.nousresearch.com/docs/user-guide/security) | 命令审批、DM 配对、容器隔离 |
| [工具与工具集](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools) | 40+ 工具、工具集系统、终端后端 |
| [技能系统](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | 过程记忆、技能中心、创建技能 |
| [记忆](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) | 持久记忆、用户画像、最佳实践 |
| [MCP 集成](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) | 连接任意 MCP 服务器扩展能力 |
| [定时调度](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) | 定时任务与平台投递 |
| [上下文文件](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) | 塑造每次对话的项目上下文 |
| [架构](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture) | 项目结构、代理循环、关键类 |
| [贡献](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) | 开发设置、PR 流程、代码风格 |
| [CLI 参考](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) | 全部命令与标志 |
| [环境变量](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) | 完整环境变量参考 |

---

## 从 OpenClaw 迁移

配置向导（`hermes setup`）会自动检测 `~/.openclaw` 并在配置开始前提示迁移。安装后迁移：

```bash
hermes claw migrate              # 交互式迁移（完整预设）
hermes claw migrate --dry-run    # 预览将被迁移的内容
hermes claw migrate --preset user-data   # 不含密钥的迁移
hermes claw migrate --overwrite  # 覆盖已有冲突
```

导入：`SOUL.md`、`MEMORY.md`、`USER.md`、用户创建技能（→ `~/.hermes/skills/openclaw-imports/`）、命令允许列表、消息设置、白名单内的 API 密钥、TTS 资产和工作区 `AGENTS.md`。

---

## 贡献

欢迎贡献。开发设置、代码风格和 PR 流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。[AGENTS.md](AGENTS.md) 中的贡献准则决定什么可合入、什么不可以——提交大型 PR 前请先阅读。

```bash
git clone https://github.com/tanzeelshujahkhan/evil-hermes.git
cd evil-hermes
uv venv ~/.hermes/venvs/hermes-dev --python 3.11
source ~/.hermes/venvs/hermes-dev/bin/activate
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

完整的 Hermes Agent 测试套件（约 17k 测试）随仓库发布于 `tests/`。

---

## 社区

- 💬 [Discord](https://discord.gg/nousresearch) — Hermes Agent 社区
- 🐛 [GitHub Issues](https://github.com/tanzeelshujahkhan/evil-hermes/issues) — 错误报告和功能请求
- 💡 [GitHub Discussions](https://github.com/tanzeelshujahkhan/evil-hermes/discussions) — 提问和设计讨论
- 📚 [技能中心](https://agentskills.io) — 代理技能开放标准

---

## 许可证

MIT — 见 [LICENSE](LICENSE)。

**由 [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan) 构建。** Fork 自 [Hermes Agent](https://github.com/NousResearch/hermes-agent)——相同引擎，主权身份，运营者拥有的策略。
