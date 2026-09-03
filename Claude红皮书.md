# Claude 红皮书：从安装到实战的全链路使用指南

> 非官方开源指南 · 持续更新版<br>
> 写给开发者、独立开发者和 AI 工具重度用户的 Claude 使用手册。

| 版本 | 最后校验 | 资料性质 |
| --- | --- | --- |
| v0.1.0 | 2026-09-03 | 非官方指南，不代表 Anthropic 官方文档或产品承诺 |

> 本文以 2026 年 9 月可访问的 Claude 应用、Claude Code、Claude API 能力为参考。相关产品更新很快，安装方式、模型名称、额度、入口位置和命令参数都可能变化；涉及具体功能和价格时，请以 [Claude Code 官方文档](https://code.claude.com/docs)、[Claude 平台文档](https://platform.claude.com)、当前版本和你账号实际显示为准。
>
> 书中提到的第三方工具、社区插件属于扩展玩法记录，不属于 Anthropic 官方功能。

## 阅读入口

- [在线阅读](https://fuzzylogic112.github.io/Auto-Data-Pipeline/)（本书网页版）
- [Markdown 原稿](https://github.com/FuzzyLogic112/Auto-Data-Pipeline/blob/main/Claude%E7%BA%A2%E7%9A%AE%E4%B9%A6.md)
- [Claude Code 官方文档](https://code.claude.com/docs)

---

# 0. 使用说明

## 0.1 重要声明

- 本资料为非官方指南，不代表 Anthropic 官方文档。
- 所有功能以官方文档和你本地的 Claude Code 实际版本为准。
- 书中所有命令、路径、字段名都标注了来源章节，建议边读边在自己的终端里验证一遍。
- Claude Code 是滚动发布的，很多能力会标注"需要 vX.Y.Z 或更高版本"。遇到命令不存在，第一反应先升级。

## 0.2 这份指南适合谁

- 完全没用过 Claude Code，但想系统上手的人。
- 会写代码，但不知道怎么把 AI 编码代理接进真实项目的人。
- 已经用过 Cursor、Copilot、Codex，想搞清楚 Claude Code 工作流差异的人。
- 想把 Claude 接进 CI/CD、做自动化流水线的人。
- 想用 Claude API 自己写应用的开发者。

不适合：想找"一句提示词生成完整 SaaS"的银弹的人。本书讲的是把 AI 当成一个需要交接上下文、需要验收、需要留下工程规范的协作者。

## 0.3 阅读路线

| 你的情况 | 建议路线 |
| --- | --- |
| 从零开始 | 第一篇 → 第二篇 → 第四篇 → 挑一个第五篇的案例做完 |
| 已经装好了，想用得更顺 | 第三篇（重点看 3.1 CLAUDE.md、3.4 Skills）→ 第四篇 |
| 想做团队规范 | 3.1 CLAUDE.md → 3.2 rules → 3.6 Hooks → 3.8 Plugins |
| 想接外部系统 | 3.7 MCP → 3.10 GitHub Actions |
| 想自己写应用 | 附录 A：Claude API 快速上手 |

**一句话建议**：先花 30 分钟把第二篇跑通，再回来读第三篇。没有跑过一次真实会话，第三篇的所有概念都会显得抽象。

---

# 第一篇：先搞懂 Claude 是什么

## 1.1 三个入口，别搞混

"Claude"是一个模型家族的名字，但你实际接触到的是三类完全不同的产品。新手最常见的困惑就是把它们混为一谈。

| 入口 | 是什么 | 典型场景 | 计费 |
| --- | --- | --- | --- |
| **Claude 应用**（网页 / 桌面 / 手机） | 对话式助手，带 Artifacts、Projects、连接器 | 写文档、做分析、生成图表、日常问答 | Free / Pro / Max / Team / Enterprise 订阅 |
| **Claude Code** | 跑在你终端（或 IDE / 网页 / CI）里的编码代理，能读写文件、执行命令、提交 Git | 改代码、修 Bug、重构、跑测试、做自动化 | 订阅额度，或 Claude Console 的 API 额度 |
| **Claude API** | 直接调 `POST /v1/messages`，你自己写应用 | 把 Claude 嵌进你的产品里 | 按 token 计费 |

本书的重心是 **Claude Code**，因为它是三者中门槛最陡、也最容易用错的一个。附录 A 单独讲 API。

Claude Code 本身也不只有终端一种形态：

- **终端 CLI**：`claude` 命令，本书的默认语境。
- **桌面应用**：macOS / Windows，图形界面。
- **VS Code / JetBrains 扩展**：在 IDE 里直接开会话。
- **Claude Code on the web**：浏览器或手机上开一个云端会话（`claude.ai/code`），仓库会在云容器里被 clone 一份。
- **Slack**：在频道里 @ 它。
- **CI/CD**：GitHub Actions、GitLab CI（见 3.10）。

## 1.2 模型家族与选型

Claude 的模型按能力和价格分档。截至本书校验时间，主要在售模型如下（价格为 Anthropic 一方 API 的每百万 token 单价，美元）：

| 模型 | 模型 ID | 上下文 | 输入 $/M | 输出 $/M |
| --- | --- | --- | --- | --- |
| Claude Fable 5.1 | `claude-fable-5-1` | 1M | 10.00 | 50.00 |
| Claude Opus 5 | `claude-opus-5` | 1M | 5.00 | 25.00 |
| Claude Opus 4.8 | `claude-opus-4-8` | 1M | 5.00 | 25.00 |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | 2.00 | 10.00 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M | 3.00 | 15.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | 1.00 | 5.00 |

> Amazon Bedrock 和 Google Vertex AI 由合作方运营，价格另计；Microsoft Foundry 按上表的一方价格通过 Microsoft Marketplace 结算。

**选型的三句话总结：**

1. **默认用 Opus 系列。** 复杂重构、跨文件推理、长任务，能力差距非常明显，省下的返工时间远超 token 差价。
2. **Sonnet 用在高频、量大的生产工作负载上。** 摘要、分类、批量改写这类任务，Sonnet 5 的性价比很好。
3. **Haiku 只用在简单且对延迟敏感的场景。** 比如一个情感分类接口。也常被拿来当 Subagent 里干粗活的"廉价工人"。

**关于 effort（推理投入档位）**：新一代模型支持 `low / medium / high / xhigh / max` 五档。档位不是越高越好——它是在同一个模型内部拿 token 花费换思考深度。编码和长周期代理任务对 effort 敏感，`xhigh` 通常是这类工作的甜点；聊天、分类这类任务在 `low`/`medium` 上质量往往不掉。在 Claude Code 里可以用 `/model` 相关配置调整。

> **一个反直觉的经验**：与其搭一条"简单任务用便宜模型、复杂任务升级到贵模型"的级联，不如先测一下"最强模型 + 低 effort"。新模型的低档位常常已经超过上一代的高档位，而且单一模型意味着单一缓存命名空间——级联会让你损失跨模型的 prompt 缓存复用。

## 1.3 Claude Code 和 Cursor / Copilot 有什么不同

这是被问得最多的问题。核心差异不在模型，而在**交互形态**。

| 维度 | 补全型工具（Copilot 等） | 编辑器内聊天（Cursor 等） | Claude Code |
| --- | --- | --- | --- |
| 主要单位 | 一行 / 一个函数 | 一个文件 / 几个选区 | 一个任务 |
| 谁决定读哪些文件 | 你（靠打开的标签页） | 你（靠 @ 引用） | 它自己（用 Glob/Grep/Read 探索） |
| 能不能执行命令 | 不能 | 有限 | 能，跑测试、装依赖、提交 Git |
| 会话终点 | 你接受补全 | 你复制粘贴 | 它跑完验证，交付一个可 review 的 diff |

**Claude Code 的心智模型是"代理循环"（agentic loop）**：你给一个目标，它自己决定调用哪些工具、读哪些文件、执行什么命令，观察结果后再决定下一步，直到任务完成或需要问你。

这带来两个直接后果：

1. **你不需要手动喂上下文。** 不用把文件粘进对话框。说"这个项目的鉴权逻辑在哪"，它会自己去搜。
2. **你需要管权限。** 因为它真的会执行 `rm`、`git push`、`npm install`。这就是第 2.5 节权限模式存在的原因。

## 1.4 内置工具：它到底能做什么

理解 Claude Code 能力边界的最快方式，是知道它手上有哪些工具：

| 工具 | 作用 |
| --- | --- |
| `Read` / `Write` / `Edit` | 读文件、写新文件、对已有文件做精确替换 |
| `Glob` / `Grep` | 按文件名模式查找、按内容正则搜索（基于 ripgrep） |
| `Bash` | 执行 shell 命令（Windows 上还有 `PowerShell`） |
| `WebFetch` / `WebSearch` | 抓取网页、搜索网络 |
| `Agent` | 派生 Subagent，把子任务扔到独立上下文里跑（见 3.5） |
| `Skill` | 调用一个 Skill（见 3.4） |
| `AskUserQuestion` | 卡在需要你拍板的决策时，弹选项问你 |
| MCP 工具 | 你接进来的外部系统能力（见 3.7） |

一个实用推论：**只要能用命令行做的事，Claude Code 大概率能做。** 部署、数据库迁移、抓日志、跑 profiler、生成图表——都不需要专门的集成，Bash 就够了。

## 1.5 上下文窗口：唯一真正稀缺的资源

每个会话有一个上下文窗口（当代模型是 1M token）。会话里的一切都要占地方：系统提示、CLAUDE.md、工具定义、你的每一句话、它读过的每个文件、每条命令的输出。

窗口填满时会触发 **自动压缩（auto-compaction）**：早期对话被摘要，腾出空间继续。压缩是有损的。

这带来三条实操纪律：

1. **一个会话干一件事。** 做完一个任务就 `/clear`，别在一个会话里从改 Bug 一路聊到重构架构。
2. **别让它读不需要读的东西。** "把整个 `logs/` 目录读一遍再告诉我哪里出错了"是在烧上下文，正确做法是让它 `grep`。
3. **重要约定写进 CLAUDE.md，不要只在对话里说。** 项目根目录的 CLAUDE.md 在压缩后会被重新读回来注入；只在对话里说过的话不会。

用 `/context` 可以随时查看当前上下文的占用分布，包括哪些 memory 文件被加载了。

---

# 第二篇：安装、配置与环境准备

## 2.1 安装前准备

- 一个终端。
- 一个真实的代码项目（不要用空目录练手，Claude Code 的价值在于理解已有代码）。
- 一个账号，三选一：
  - **Claude 订阅**（Pro / Max / Team / Enterprise）——推荐，额度按订阅算。
  - **Claude Console 账号**——按 API 用量预付费。首次登录会自动建一个叫 "Claude Code" 的 workspace 方便统一看成本。
  - **云厂商通道**——Amazon Bedrock、Google Cloud Agent Platform、Microsoft Foundry。

## 2.2 安装 Claude Code

**原生安装（推荐，会自动后台更新）**

macOS / Linux / WSL：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://claude.ai/install.ps1 | iex
```

Windows CMD：

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

> 如果报 `The token '&&' is not a valid statement separator`，说明你在 PowerShell 而不是 CMD；如果报 `'irm' is not recognized`，说明你在 CMD 而不是 PowerShell。提示符带 `PS C:\` 的是 PowerShell。

**包管理器安装（不会自动更新，要手动升级）**

```bash
# macOS
brew install --cask claude-code          # 稳定通道，通常落后一周左右
brew install --cask claude-code@latest   # 最新通道

# Windows
winget install Anthropic.ClaudeCode

# Debian / Fedora / RHEL / Alpine 也支持 apt、dnf、apk
```

**验证安装**

```bash
claude --version
```

正常会输出版本号加 `(Claude Code)`。

> 原生 Windows 上建议装一个 [Git for Windows](https://git-scm.com/downloads/win)，这样 Claude Code 才能用 Bash 工具；没装的话它会退化成用 PowerShell。WSL 环境不需要。

## 2.3 登录

```bash
claude
```

首次运行会引导你在浏览器里完成认证。想换账号或重新认证，在会话里输入：

```
/login
```

> 如果你设置了 `ANTHROPIC_API_KEY` 环境变量，Claude Code 会跳过登录流程，转而让你确认这个 key。这也是排查"我明明订阅了却在扣 API 费用"的第一个检查点。

## 2.4 第一次会话

```bash
cd /path/to/your/project
claude
```

进去之后建议按这个顺序走一遍：

```
这个项目是做什么的？
```

```
主入口在哪里？解释一下目录结构
```

```
给主文件加一个 hello world 函数
```

```
我改了哪些文件？
```

```
把改动提交上去，写一条描述清楚的 commit message
```

跑完这五步，你就已经用过 Claude Code 的全部核心循环了：探索 → 理解 → 修改 → 检查 → 交付。

**几个必知的快捷键：**

- `/` — 列出所有可用命令和 Skill
- `Tab` — 命令补全
- `↑` — 历史命令
- `Shift+Tab` — 循环切换权限模式
- `Esc` — 打断当前操作
- `Ctrl+D` 按两次 — 退出

## 2.5 权限模式：最该先搞懂的一件事

权限模式决定"哪些操作不用问你就能做"。用 `Shift+Tab` 循环切换，或启动时用 `--permission-mode` 指定。

| 模式 | 配置值 | 不用问就能做的事 | 适合 |
| --- | --- | --- | --- |
| Manual（手动） | `default` | 只有读操作 | 敏感改动、不熟悉的代码 |
| 接受编辑 | `acceptEdits` | 读、改文件、常见文件系统命令（`mkdir`/`mv`/`cp` 等） | 一边 review 一边迭代 |
| 计划 | `plan` | 读，以及分类器批准的命令 | 动手前先摸清代码库 |
| 自动 | `auto` | 几乎全部，由一个分类器模型在后台做安全审查 | 长任务，减少打断 |
| 仅预批准 | `dontAsk` | 只有你事先允许的工具 | 锁死的 CI 和脚本 |
| 跳过检查 | `bypassPermissions` | 全部 | **只在隔离容器 / 虚拟机里用** |

在 Pro、Max、Team 计划上，交互式终端会话默认从 **auto 模式**起步（需要 v2.1.228+，原生 Windows 需 v2.1.233+）；其他计划默认从 Manual 起步。

**有几件事任何模式都不会自动放行**，包括 `bypassPermissions`：

- 你显式配了 ask 规则的工具
- 需要用户交互的工具（比如 `AskUserQuestion`）
- 针对关键路径的 `rm` / `rmdir`

**实操建议：**

- 日常开发：`auto`。
- 改生产配置、动数据库迁移、碰 CI 脚本：切回 `default`，一步步看。
- 探索陌生代码库、想先要一份方案再动手：`plan`。
- CI 里：`dontAsk` 配一份精确的 `--allowedTools` 白名单。

```bash
# CI 里的典型写法
claude -p "run the test suite" --permission-mode dontAsk --allowedTools "Bash(npm test)" "Read"
```

> `--dangerously-skip-permissions`（即 `bypassPermissions`）只应该在容器、虚拟机或沙箱运行时里用，并且在 Linux/macOS 上以非 root 用户运行。不要在你的日常开发机上开这个。

模式设定的是基线，你还可以叠加**权限规则**做精细控制。deny 规则在所有模式下都生效，包括 `bypassPermissions`；allow 规则在 `bypassPermissions` 下无意义。

## 2.6 命令速查

**Shell 命令（在终端里敲，用来启动会话）**

| 命令 | 作用 |
| --- | --- |
| `claude` | 启动交互式会话 |
| `claude "任务描述"` | 带初始提示启动 |
| `claude -p "问题"` | 跑一次就退出（非交互 / headless 模式） |
| `claude -c` | 继续当前目录最近的一次会话 |
| `claude -r` | 从历史会话里挑一个恢复 |
| `claude --permission-mode plan` | 指定启动的权限模式 |
| `claude --model claude-opus-5` | 指定模型 |
| `claude --add-dir ../shared` | 额外授权一个工作目录 |
| `claude mcp add ...` | 添加 MCP 服务器（见 3.7） |
| `claude setup-token` | 生成长期有效的订阅 token（给 CI 用） |

**会话命令（进去之后敲）**

| 命令 | 作用 |
| --- | --- |
| `/help` | 列出所有命令 |
| `/clear` | 清空对话历史，开新话题 |
| `/compact` | 手动触发上下文压缩 |
| `/context` | 查看上下文占用分布和已加载的 memory 文件 |
| `/init` | 自动生成 CLAUDE.md |
| `/memory` | 浏览、编辑各层级的 memory 文件 |
| `/model` | 切换模型 / 调 effort |
| `/mcp` | 查看和管理 MCP 服务器 |
| `/hooks` | 浏览已配置的 Hooks（只读） |
| `/skills` | 查看可用的 Skill |
| `/doctor` | 配置体检，会给出修复建议 |
| `/login` | 重新认证 |
| `/resume` | 恢复历史会话 |
| `/install-github-app` | 一键配置 GitHub Actions 集成 |
| `/exit` | 退出 |

> `/doctor` 是被严重低估的命令。配置不生效、CLAUDE.md 没加载、hook 不触发，先跑它。

## 2.7 项目配置文件都在哪

Claude Code 的配置分散在几个位置，搞清楚这张表能省掉大量困惑：

| 路径 | 作用域 | 该放什么 |
| --- | --- | --- |
| `~/.claude/settings.json` | 你的所有项目 | 个人偏好、个人 Hooks |
| `~/.claude/CLAUDE.md` | 你的所有项目 | 个人编码风格偏好 |
| `~/.claude/skills/<name>/SKILL.md` | 你的所有项目 | 个人 Skill |
| `~/.claude/agents/<name>.md` | 你的所有项目 | 个人 Subagent |
| `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 当前项目，**入库共享** | 项目架构、构建命令、团队规范 |
| `./CLAUDE.local.md` | 当前项目，**加 .gitignore** | 你个人的沙箱地址、测试数据 |
| `./.claude/rules/*.md` | 当前项目，入库共享 | 按路径生效的分主题规则 |
| `./.claude/settings.json` | 当前项目，入库共享 | 团队共享的 Hooks、权限规则 |
| `./.claude/settings.local.json` | 当前项目，不入库 | 你个人的本地覆盖 |
| `./.claude/skills/<name>/SKILL.md` | 当前项目，入库共享 | 项目专属流程 |
| `./.claude/agents/<name>.md` | 当前项目，入库共享 | 项目专属 Subagent |
| `./.mcp.json` | 当前项目，入库共享 | 团队共享的 MCP 服务器 |

一个健康的项目，`.claude/` 目录应该是**入库的**——它是团队协作资产的一部分，跟 `.eslintrc` 是同一个性质的东西。

---

# 第三篇：核心能力详解

这一篇是本书的主体。六个扩展机制——CLAUDE.md、rules、Skills、Subagents、Hooks、MCP——解决的是不同问题，选错了会很别扭。先看这张决策表：

| 你想要的 | 用哪个 | 为什么 |
| --- | --- | --- |
| 每次会话都要知道的事实（构建命令、目录约定） | **CLAUDE.md** | 启动时加载，永远在场 |
| 只在改某类文件时才需要的规范 | **`.claude/rules/` + `paths`** | 按路径懒加载，省上下文 |
| 一套重复的多步流程 | **Skill** | 调用时才加载正文，平时几乎不占上下文 |
| 一个会吃掉大量上下文的子任务 | **Subagent** | 独立上下文，只把结论带回来 |
| 必须每次都发生的确定性动作 | **Hook** | shell 命令，不依赖模型的判断 |
| 接外部系统（数据库、Jira、Slack） | **MCP** | 标准协议，一次接入到处可用 |
| 把上面这些打包分发给团队 | **Plugin** | 一个仓库装完所有配置 |

**最重要的一条判断准则**：CLAUDE.md 是**事实**，Skill 是**流程**，Hook 是**规则**。如果你发现 CLAUDE.md 里出现了"第一步……第二步……"，那它应该是个 Skill；如果出现了"每次都必须……"，那它应该是个 Hook。

## 3.1 CLAUDE.md：项目记忆

CLAUDE.md 是一个普通的 Markdown 文件，Claude 在每次会话开始时读它。它是你把"要反复解释的东西"写下来的地方。

**什么时候该往里加东西：**

- Claude 第二次犯同一个错。
- Code review 抓出了一个它本该知道的项目约定。
- 你这次会话又打了一遍上次打过的纠正。
- 一个新同事需要同样的背景才能上手。

**生成初稿：**

```
/init
```

Claude 会分析代码库，生成一份带构建命令、测试指令、项目约定的 CLAUDE.md。如果已经有了，`/init` 会给改进建议而不是覆盖。

> 设置 `CLAUDE_CODE_NEW_INIT=1` 可以开启交互式多阶段流程：它会问你要不要顺便配 Skill 和 Hook，用 Subagent 探索代码库，补问缺失信息，最后给你一份可 review 的提案再落盘。

### 加载顺序与优先级

CLAUDE.md 可以放在多个位置，按作用域从宽到窄加载：

| 层级 | 位置 | 用途 |
| --- | --- | --- |
| 组织策略 | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`<br>Linux/WSL `/etc/claude-code/CLAUDE.md`<br>Windows `C:\Program Files\ClaudeCode\CLAUDE.md` | 全公司统一规范，个人无法排除 |
| 用户 | `~/.claude/CLAUDE.md` | 你的个人偏好，跨所有项目 |
| 项目 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队共享，入版本库 |
| 本地 | `./CLAUDE.local.md` | 个人的项目内偏好，加 `.gitignore` |

**关键机制**：所有找到的文件是**拼接**进上下文，不是相互覆盖。从文件系统根目录往下到你的工作目录依次排列，所以越靠近你启动位置的指令越靠后被读到。同一目录内 `CLAUDE.local.md` 排在 `CLAUDE.md` 之后。

工作目录**下面**的子目录里的 CLAUDE.md 不在启动时加载，而是在 Claude 读到那个子目录的文件时才载入——这是 monorepo 的关键机制。

### 写出真正被遵守的指令

CLAUDE.md 是作为上下文注入的，不是强制配置。写法直接影响遵守率。

**篇幅**：每个文件控制在 **200 行以内**。文件越长，占用上下文越多，遵守度反而下降。

**具体**：写能被验证的指令。

```markdown
✅ 用 2 空格缩进
✅ 提交前跑 `npm test`
✅ API handler 放在 `src/api/handlers/`

❌ 代码要格式化好
❌ 记得测试
❌ 保持文件组织有序
```

**一致**：两条规则互相矛盾时，Claude 可能随机挑一条。定期清理过期和冲突的条目。

**HTML 注释会被剥离**：块级 `<!-- 维护者备注 -->` 在注入前会被去掉，可以用来给人类留言而不消耗 token。

### 导入其他文件

用 `@path/to/file` 语法导入，相对路径相对于**包含它的文件**解析，最多递归 4 层：

```markdown
项目概览见 @README，可用命令见 @package.json。

# 补充规范
- Git 工作流 @docs/git-instructions.md
```

> 想在 CLAUDE.md 里提到一个路径但不想导入它，用反引号包起来：写 `` `@README` `` 是纯文本，写 `@README` 就会真的导入。
>
> 注意：导入的文件仍然会在启动时全量进上下文，所以拆分 import 只是组织形式上的整洁，**并不省上下文**。真正省上下文的是下一节的路径规则。

### 已经有 AGENTS.md 怎么办

Claude Code 只读 `CLAUDE.md`，不读 `AGENTS.md`。如果你的仓库已经在用 AGENTS.md，建一个 CLAUDE.md 导入它：

```markdown
@AGENTS.md

## Claude Code 专属

改 `src/billing/` 下的代码时先用 plan 模式。
```

也可以直接软链（Windows 上需要管理员权限或开发者模式，建议还是用 import）：

```bash
ln -s AGENTS.md CLAUDE.md
```

`/init` 还会读 Cursor 规则（`.cursor/rules/`、`.cursorrules`）和 Copilot 规则（`.github/copilot-instructions.md`）并吸收进去。`/import` 命令（需 v2.1.213+）能把其他编码代理的配置——指令文件、MCP 服务器、命令、Subagent、Skill——一次性搬过来。

### 一份能用的 CLAUDE.md 模板

```markdown
# 项目名

一句话说清这个项目是干什么的。

## 构建与测试

- 安装依赖：`pnpm install`
- 开发服务器：`pnpm dev`（跑在 3000 端口）
- 单元测试：`pnpm test`
- 只跑改动的包：`pnpm test --filter=<pkg>`
- 提交前必须通过：`pnpm lint && pnpm typecheck && pnpm test`

## 目录约定

- `src/api/handlers/` — HTTP 路由处理
- `src/domain/` — 纯业务逻辑，不允许 import 任何 IO 模块
- `src/infra/` — 数据库、外部服务客户端
- `tests/fixtures/` — 测试数据，不要在测试文件里内联大对象

## 约定

- 用 2 空格缩进，不用 tab。
- 新增依赖前先问，这个项目刻意保持依赖精简。
- 数据库改动必须配一个 migration 文件，不要直接改 schema.sql。
- 错误信息面向用户，不要把 stack trace 透出到 API 响应里。

## 已知坑

- `src/legacy/report.ts` 有一套自己的日期处理，不要用 date-fns 去"统一"它，
  下游有三个报表依赖它现在的时区行为。
- CI 上 `test:e2e` 偶发超时，重跑一次通常就好，不要改超时阈值。
```

注意最后一节。**"已知坑"往往是整份 CLAUDE.md 里价值最高的部分**——那是 Claude 从代码里推不出来的东西。

## 3.2 `.claude/rules/`：按路径生效的规则

项目一大，CLAUDE.md 就会撑爆。`.claude/rules/` 让你把指令拆成分主题的文件，并且**按文件路径条件加载**。

```
your-project/
├── .claude/
│   ├── CLAUDE.md
│   └── rules/
│       ├── code-style.md
│       ├── testing.md
│       └── api-design.md
```

不带 `paths` 前置元数据的规则在启动时加载，优先级和 `.claude/CLAUDE.md` 相同。带 `paths` 的只在 Claude 读到匹配文件时才载入：

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API 开发规范

- 所有端点必须做入参校验
- 用统一的错误响应格式
- 补 OpenAPI 注释
```

支持的 glob 模式：

| 模式 | 匹配 |
| --- | --- |
| `**/*.ts` | 任意目录下的所有 TypeScript 文件 |
| `src/**/*` | `src/` 下的所有文件 |
| `*.md` | 项目根目录的 Markdown 文件 |
| `src/components/*.tsx` | 特定目录的 React 组件 |

支持花括号展开：`src/**/*.{ts,tsx}`。注意展开有预算上限（单条规则 1000 个展开模式 / 4 MiB），超了就按字面量处理，那样是匹配不到文件的。

`~/.claude/rules/` 放个人规则，作用于你机器上的所有项目，加载顺序在项目规则之前（所以项目规则优先级更高）。

`.claude/rules/` 支持软链，可以维护一套共享规则链进多个项目：

```bash
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

> **rules vs skills**：rules 是每次（或每次碰到匹配文件时）都进上下文的**约束**；skill 是只在被调用时才加载的**流程**。不确定的时候问自己："这条内容需要在 Claude 没主动想到它的时候也生效吗？"需要就是 rule，不需要就是 skill。

## 3.3 自动记忆

除了你写的 CLAUDE.md，Claude 还会自己记笔记。它保存四类信息：

- `user` — 你的角色、专长、工作偏好
- `feedback` — 你给它的纠正，以及你确认过的做法
- `project` — 进行中的工作、截止日期、代码和 git 历史里推不出来的决策
- `reference` — 项目外的信息在哪找，比如 issue tracker、监控面板

它会**跳过**任何能从代码库推导出来的东西（架构、文件路径、调试修复），也会跳过 CLAUDE.md 里已经写了的内容。

**存储位置**：`~/.claude/projects/<project>/memory/`，其中 `MEMORY.md` 是索引，每条记忆一行，会话开始时加载（前 200 行或 25KB，以先到者为准）；具体内容放在同目录的主题文件里，按需读取。

自动记忆默认开启。关闭方式：

```json
{
  "autoMemoryEnabled": false
}
```

或设环境变量 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`。用 `/memory` 可以浏览、编辑、删除这些文件——全是纯 Markdown。

> **重要边界**：自动记忆是**机器本地**的。同一个 git 仓库的所有 worktree 和子目录共享一个记忆目录，但不会跨机器同步，也不会进云端会话。真正需要团队共享的知识，写进 CLAUDE.md。

## 3.4 Skills：把重复流程变成一条斜杠命令

Skill 是一个带 YAML 前置元数据的 `SKILL.md` 文件。你可以用 `/skill-name` 直接调用，Claude 也可以在判断相关时自动加载。

**什么时候该建 Skill**：你第三次把同一段说明粘进对话框的时候；或者 CLAUDE.md 里某一节已经长成了一套流程而不是一条事实的时候。

Skill 相比 CLAUDE.md 的关键优势：**正文只在被调用时才加载**，所以再长的参考资料平时也几乎不占上下文。

### 存放位置

| 层级 | 路径 | 作用于 |
| --- | --- | --- |
| 企业 | 由 managed settings 部署 | 组织内所有人 |
| 个人 | `~/.claude/skills/<name>/SKILL.md` | 你的所有项目 |
| 项目 | `.claude/skills/<name>/SKILL.md` | 当前项目 |
| 插件 | `<plugin>/skills/<name>/SKILL.md` | 启用插件的地方 |

同名冲突时：企业 > 个人 > 项目。插件 Skill 用 `plugin-name:skill-name` 命名空间，不会冲突。

> `.claude/commands/` 里的自定义命令已经和 Skill 合并了。`.claude/commands/deploy.md` 和 `.claude/skills/deploy/SKILL.md` 都会产生 `/deploy`，行为一致。旧的 commands 文件继续可用，但新写的建议用 Skill——它支持配套文件、调用控制、自动加载。

### 一个最小可用的 Skill

```bash
mkdir -p ~/.claude/skills/summarize-changes
```

`~/.claude/skills/summarize-changes/SKILL.md`：

```markdown
---
description: 总结未提交的改动并标出风险点。当用户问改了什么、想要 commit message、或让你 review diff 时使用。
---

## 当前改动

!`git diff HEAD`

## 指令

用两三个要点总结上面的改动，然后列出你注意到的风险：缺失的错误处理、
硬编码的值、需要一并更新的测试。如果 diff 为空，直接说没有未提交的改动。
```

这里的 `` !`git diff HEAD` `` 是**动态上下文注入**：Claude Code 会先执行这条命令，把输出替换到原位，然后才把内容交给 Claude。所以 Claude 拿到的是真实的 diff，不是一句"你去跑 git diff"。

### 前置元数据字段

全部字段都是可选的，但 `description` 强烈建议写——Claude 靠它判断什么时候该用这个 Skill。

| 字段 | 说明 |
| --- | --- |
| `name` | 显示名，默认取目录名 |
| `description` | 做什么、什么时候用。把关键场景写在最前面：`description` 和 `when_to_use` 合并后在列表里会被截断到 1536 字符 |
| `when_to_use` | 补充触发场景、示例请求 |
| `argument-hint` | 自动补全时的参数提示，如 `[issue-number]` |
| `arguments` | 命名位置参数，供 `$name` 替换 |
| `disable-model-invocation` | 设 `true` 则只有你能调用，Claude 不会自动加载 |
| `user-invocable` | 设 `false` 则只有 Claude 能调用，不出现在 `/` 菜单里 |
| `allowed-tools` | 调用这个 Skill 的那一轮里免授权的工具 |
| `disallowed-tools` | 这个 Skill 活跃期间从工具池里移除的工具 |
| `model` | 这个 Skill 活跃时用哪个模型 |
| `effort` | 覆盖会话的 effort 档位 |
| `context` | 设 `fork` 则在派生的 Subagent 上下文里跑 |
| `paths` | glob 模式，限制自动触发的范围 |
| `hooks` | 调用时注册、之后整个会话保持的 Hook |

### 控制"谁能调用"

这是很多人踩坑的地方。两个字段的组合效果：

| 前置元数据 | 你能调用 | Claude 能调用 | 什么时候进上下文 |
| --- | --- | --- | --- |
| （默认） | 能 | 能 | description 常驻，正文调用时加载 |
| `disable-model-invocation: true` | 能 | **不能** | description 不进上下文，你调用时才加载正文 |
| `user-invocable: false` | **不能** | 能 | description 常驻，正文调用时加载 |

**`disable-model-invocation: true` 用于有副作用的操作**——`/commit`、`/deploy`、`/send-slack-message`。你不希望 Claude 觉得"代码看起来挺好的"就自己去部署了。

```markdown
---
name: deploy
description: 把应用部署到生产环境
disable-model-invocation: true
allowed-tools: Bash(./scripts/deploy.sh *) Bash(git status *)
---

把 $ARGUMENTS 部署到生产环境：

1. 跑完整测试套件
2. 构建
3. 推到部署目标
4. 验证部署成功
```

### 传参数

`$ARGUMENTS` 接收 Skill 名后面的全部内容；`$ARGUMENTS[N]` 或简写 `$N` 按位置取：

```markdown
---
name: migrate-component
description: 把组件从一种语言迁移到另一种
---

把 $0 组件从 $1 迁移到 $2。保留全部现有行为和测试。
```

`/migrate-component SearchBar JavaScript TypeScript` 就会替换成对应的三个值。

你还可以在一条消息开头**叠加**多个 Skill：`/write-tests /fix-issue 123` 会同时加载两个 Skill，并把 `123` 作为 `$ARGUMENTS` 传给两者。

### `allowed-tools` 的安全提示

`allowed-tools` 授予的是**调用那一轮**的免授权，你发下一条消息时就失效了。

⚠️ 但要注意：**工作区信任对这个字段不设防**。项目里一个 Skill 的 `allowed-tools` 会在你或 Claude 调用它时直接生效，包括在你从未信任过的目录里跑 `-p`。**在一个陌生仓库里跑 Claude Code 之前，先看看它的 `.claude/skills/` 里都写了什么。**

## 3.5 Subagents：把脏活扔进独立上下文

Subagent 是一个在**独立上下文窗口**里跑的子代理。它读一堆文件、跑一堆命令，最后只把结论带回主会话。

**它解决的核心问题是上下文污染**。"在这 200 个文件里找出所有还在用旧版鉴权 API 的地方"——如果在主会话里干，200 个文件的内容会永久占据你的上下文；扔给 Subagent，你只会拿回一份清单。

### 定义位置

| 位置 | 作用域 | 优先级 |
| --- | --- | --- |
| Managed settings | 组织级 | 1（最高） |
| `--agents` CLI 参数 | 当前会话 | 2 |
| `.claude/agents/` | 当前项目 | 3 |
| `~/.claude/agents/` | 你的所有项目 | 4 |
| 插件的 `agents/` 目录 | 启用插件处 | 5（最低） |

### 文件格式

```markdown
---
name: code-reviewer
description: 审查代码质量和最佳实践。新代码写完后主动使用。
tools: Read, Grep, Glob, Bash
model: sonnet
---

你是一名代码审查员。被调用时，分析代码并给出关于质量、安全性
和最佳实践的具体、可操作的反馈。每条问题都要说明：问题是什么、
当前代码长什么样、改成什么样。
```

**必填字段**：

- `name` — 小写字母加连字符，不能含 `:`（那是插件命名空间的保留字符）
- `description` — 解释什么时候该委派给它。写上 "use proactively" 之类的措辞能提高被自动调用的概率。所有 Subagent 的 description 共享一个 15000 token 的预算，所以要简洁。

**重要可选字段**：

| 字段 | 作用 |
| --- | --- |
| `tools` | 工具白名单，如 `Read, Grep, Glob, Bash` |
| `disallowedTools` | 工具黑名单，如 `Write, Edit` |
| `model` | `sonnet` / `opus` / `haiku` / `fable`，或完整模型 ID |
| `permissionMode` | `default` / `acceptEdits` / `auto` / `dontAsk` / `bypassPermissions` / `plan` |
| `maxTurns` | 最多几轮后停止 |
| `skills` | 预加载哪些 Skill 到它的上下文 |
| `memory` | 独立的持久记忆作用域 |
| `effort` | 覆盖会话的 effort 档位 |
| `isolation` | 设 `worktree` 则在独立的 git worktree 里跑 |

> Subagent 不能用 `AskUserQuestion` 等需要用户交互的工具——它跑在后台，没人能回答它。设计 Subagent 的提示词时，要让它在信息不足时**在报告里说明**，而不是等着提问。

模型解析顺序：单次调用的 `model` 参数 > Subagent 定义里的 `model` > `CLAUDE_CODE_SUBAGENT_MODEL` 环境变量 > 主会话的模型。

### 调用方式

```text
# 自然语言（Claude 自行判断）
用 code-reviewer 看一下我最近的改动

# @ 提及（保证调用）
@agent-code-reviewer 分析一下 auth 模块
```

也可以整个会话默认用某个 Subagent：

```bash
claude --agent code-reviewer
```

### 两个高价值的 Subagent 模板

**探索型**（读多写少，跑便宜模型）：

```markdown
---
name: explorer
description: 在大代码库里做广度搜索。当回答问题需要扫大量文件、
  而你只要结论不要文件内容时使用。
tools: Read, Grep, Glob
model: haiku
---

你负责定位代码，不负责评审代码。

1. 用 Grep 和 Glob 缩小范围，不要盲目 Read 整个目录。
2. 只读你真正需要的片段。
3. 报告格式：每条一行 `path:line — 一句话说明`。
4. 如果找不到，明确说没找到，不要猜测。
```

**验收型**（写完之后跑，独立上下文避免自我确认偏误）：

```markdown
---
name: verifier
description: 独立验证一处改动是否真的生效。改完代码后主动使用。
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: default
---

你不知道这处改动是谁做的，也不要假设它是对的。

1. 读改动涉及的文件。
2. 跑项目的测试和 lint。
3. 针对改动的行为，找出至少一个没被测试覆盖的边界情况。
4. 报告：测试是否通过（贴真实输出）、发现的问题、你的判断依据。

不要修任何东西。你的职责是报告。
```

## 3.6 Hooks：确定性的自动化

CLAUDE.md 和 Skill 都是**建议**——模型可能遵守也可能不遵守。Hook 是**保证**：它是在生命周期固定节点执行的 shell 命令，跟模型怎么想没关系。

**判断准则**：如果一件事必须在某个精确时刻发生（每次提交前、每次编辑后），写 Hook，不要写进 CLAUDE.md。

### 配置位置

| 位置 | 作用域 | 可共享 |
| --- | --- | --- |
| `~/.claude/settings.json` | 你的所有项目 | 否 |
| `.claude/settings.json` | 单个项目 | 是，可入库 |
| `.claude/settings.local.json` | 单个项目 | 否 |
| Managed policy settings | 组织级 | 是，管理员控制 |
| 插件的 `hooks/hooks.json` | 启用插件处 | 是 |
| Skill / Subagent 前置元数据 | 调用后的会话内 / 该 Subagent 运行期间 | 是 |

### JSON 结构

所有事件都是同一个 `hooks` 对象下的键：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code 需要你的确认\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

注意：Hook 的输入是通过 **stdin 传 JSON** 的，所以上面那条 `PostToolUse` 用 `jq` 从 stdin 里取出被编辑的文件路径，再交给 prettier。

### 主要事件

| 事件 | 触发时机 |
| --- | --- |
| `SessionStart` | 会话开始或恢复时 |
| `UserPromptSubmit` | 你提交提示后、Claude 处理前 |
| `PreToolUse` | 工具调用执行前，**可以拦截** |
| `PermissionRequest` | 工具调用需要权限决策时 |
| `PermissionDenied` | auto 模式拒绝了一次工具调用 |
| `PostToolUse` | 工具调用成功后 |
| `PostToolUseFailure` | 工具调用失败后 |
| `PostToolBatch` | 一批并行工具调用全部完成后 |
| `Notification` | Claude Code 发通知时 |
| `SubagentStart` / `SubagentStop` | Subagent 启动 / 结束 |
| `Stop` | Claude 回答完毕时，**可以要求它继续干** |
| `PreCompact` / `PostCompact` | 上下文压缩前 / 后 |
| `InstructionsLoaded` | CLAUDE.md 或 rules 文件被加载进上下文时（调试配置神器） |
| `FileChanged` | 被监视的文件在磁盘上变化时（`matcher` 指定文件名） |
| `SessionEnd` | 会话结束时 |

完整列表还包括 `Setup`、`UserPromptExpansion`、`MessageDisplay`、`TaskCreated`、`TaskCompleted`、`StopFailure`、`TeammateIdle`、`ConfigChange`、`CwdChanged`、`DirectoryAdded`、`WorktreeCreate`、`WorktreeRemove`、`PreModelSwitch`、`PostModelSwitch`、`Elicitation`、`ElicitationResult`。

### 三个立刻能用的 Hook

**1. 编辑后自动格式化**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "jq -r '.tool_input.file_path' | grep -E '\\.(ts|tsx|js|jsx)$' | xargs -r npx prettier --write"
        }]
      }
    ]
  }
}
```

**2. 拦截危险命令**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "jq -r '.tool_input.command' | grep -qE 'git push .*(main|master)' && echo '禁止直接推送到主分支' >&2 && exit 2 || exit 0"
        }]
      }
    ]
  }
}
```

`PreToolUse` 的 Hook 以退出码 2 结束会**阻断**这次工具调用，stderr 的内容会回传给 Claude。

**3. 用模型做判断的 Hook**

有些判断是没法用 shell 写死的。`type: "prompt"` 的 Hook 会把你的提示和 Hook 输入交给一个 Claude 模型（默认 Haiku）来决策，模型只需要返回 JSON：`"ok": true` 放行，`"ok": false` 加上 `reason` 拦截。

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [{
          "type": "prompt",
          "prompt": "检查这次会话里被要求的任务是否都完成了。如果还有明确要求但没做的，返回 ok:false 并在 reason 里说明下一步该做什么。"
        }]
      }
    ]
  }
}
```

`Stop` 事件上返回 `ok: false` 时，`reason` 会被喂回给 Claude 让它继续干活——除非响应里同时设了 `"impossible": true`，那样才允许它停。

用 `/hooks` 可以浏览所有已配置的 Hook（只读，改要直接编辑 JSON 或让 Claude 改）。要全局关掉：`"disableAllHooks": true`。

## 3.7 MCP：把外部系统接进来

MCP（Model Context Protocol）是一个开放标准，用来把 Claude Code 连到外部工具、数据库、API。接了 GitHub 的 MCP 服务器，你就能说"看一下 PR #456 提点意见"；接了数据库的，就能说"这个月的总营收是多少"。

### 传输方式

| 传输 | 适用 | 参数 |
| --- | --- | --- |
| HTTP | 远程云服务（推荐） | `--transport http` |
| SSE | Server-Sent Events（已废弃） | `--transport sse` |
| stdio | 本机进程 | `--transport stdio` |
| WebSocket | 持久双向连接 | 只能在 `.mcp.json` 里配 |

### 添加服务器

```bash
# HTTP，最常见
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# 带认证头
claude mcp add --transport http notion https://mcp.notion.com/mcp \
  --header "Authorization: Bearer YOUR_TOKEN"

# stdio，注意 -- 分隔符：后面的内容原样传给服务器命令
claude mcp add --transport stdio airtable -- npx -y airtable-mcp-server

# 带环境变量
claude mcp add --env AIRTABLE_API_KEY=YOUR_KEY --transport stdio airtable \
  -- npx -y airtable-mcp-server
```

⚠️ **stdio 的 `--` 分隔符是最常见的坑。** 没有它，Claude Code 会把 `-y` 当成自己的参数解析。

### 作用域

| 作用域 | 存放位置 | 可见性 | 用途 |
| --- | --- | --- | --- |
| `local`（默认） | `~/.claude.json` | 仅当前项目，私有 | 个人工具、实验 |
| `project` | 仓库根的 `.mcp.json` | 通过 git 共享 | 团队协作 |
| `user` | `~/.claude.json` | 你的所有项目 | 跨项目通用工具 |

```bash
claude mcp add --transport http github --scope project https://api.githubcopilot.com/mcp/
```

优先级：Local > Project > User > 插件 > claude.ai 连接器。

### `.mcp.json` 格式

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": { "Authorization": "Bearer ${GITHUB_TOKEN}" }
    },
    "database": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub"],
      "env": { "DB_URL": "${DB_URL}" }
    }
  }
}
```

支持环境变量展开，还支持默认值语法 `${API_BASE_URL:-https://api.example.com}`。

⚠️ **不要把 token 明文写进 `.mcp.json` 然后提交。** 用 `${VAR}` 展开，把真实值放在环境变量或 `.env` 里。

### 管理命令

```bash
claude mcp list                      # 列出所有服务器
claude mcp get <name>                # 看某个服务器的详情
claude mcp remove <name>             # 删除
claude mcp login <name>              # 走 OAuth 认证
claude mcp reset-project-choices     # 重置项目级服务器的信任选择
claude mcp add-from-claude-desktop   # 从 Claude 桌面版导入
```

会话里用 `/mcp` 查看连接状态：`✔ Connected`、`! Needs authentication`、`✘ Failed to connect`、`⏸ Pending approval`。

> 项目级 `.mcp.json` 里的服务器需要你在交互式会话里确认信任才会启用。这是一道有意设的防线：一个 MCP 服务器能读你的数据、发你的请求，不该因为你 clone 了一个仓库就自动生效。

## 3.8 Plugins：把配置打包分发

前面所有东西——Skill、Subagent、Hook、MCP 配置——都可以打包成一个 Plugin，通过一个 Git 仓库（marketplace）分发。

典型场景：公司有一套统一的代码审查流程、部署流程、安全检查。与其让每个人手动往 `.claude/` 里复制文件，不如做成插件，一条命令装完。

插件里的 Skill 使用 `plugin-name:skill-name` 命名空间，所以永远不会和你自己的 Skill 冲突。在 GitHub Actions 里也能直接装（见 3.10）：

```yaml
plugin_marketplaces: "https://github.com/anthropics/claude-code.git"
plugins: "code-review@claude-code-plugins"
```

注意 `plugins` 输入的格式是 `plugin-name@marketplace-name`，其中 marketplace 名来自它自己的清单文件，**不是仓库 URL**。

## 3.9 Git 与 GitHub 工作流

Claude Code 把 Git 操作变成了对话：

```text
我改了哪些文件？
把改动提交上去，写一条描述清楚的 commit message
新建一个分支叫 feature/xxx
看一下最近 5 条提交
帮我解决这些合并冲突
```

**几条实操经验：**

1. **让它自己写 commit message。** 它刚做完这些改动，比你更清楚改了什么。但要在 CLAUDE.md 里约定格式（Conventional Commits 之类）。
2. **不要让它直接推主分支。** 用 3.6 里那个 `PreToolUse` Hook 拦掉。
3. **合并冲突是它的强项。** 它能同时读懂两边的意图。但两边改了同一段逻辑、选任何一边都会丢行为时，它应该来问你——如果它没问就自己选了，在 CLAUDE.md 里加一条规则。
4. **大重构前先建分支。** 一句"先建个分支再动手"能省掉很多麻烦。

## 3.10 GitHub Actions：让 Claude 在云端干活

[claude-code-action](https://github.com/anthropics/claude-code-action) 让 Claude Code 跑在你仓库的 workflow 里。在 PR 或 issue 评论里 `@claude`，它会分析代码、实现改动、推提交。

### 快速配置

在本地仓库里跑：

```
/install-github-app
```

需要先装好 [GitHub CLI](https://cli.github.com) 并 `gh auth login`。这条命令会装好 Claude GitHub App、配好认证 secret、推一个带 workflow 文件的分支并打开 PR 页面。你需要仓库的 admin 权限。

认证 secret 二选一：

- `ANTHROPIC_API_KEY` — 来自 [Claude Console](https://platform.claude.com) 的 API key
- `CLAUDE_CODE_OAUTH_TOKEN` — 用订阅认证的 OAuth token，本地跑 `claude setup-token` 生成

### 最小可用 workflow

`.github/workflows/claude.yml`：

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
      id-token: write
      actions: read
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 1
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

几个不是模板样板的行：

- `id-token: write` — 默认的 GitHub App 认证需要它
- `actions: read` — 让 Claude 能读 PR 上的 CI 结果
- `actions/checkout` — 给它一份本地仓库副本
- `if:` — 避免不含 `@claude` 的评论也去开 runner

配好之后在任意 issue 或 PR 评论里：

```text
@claude 根据 issue 描述实现这个功能
@claude 这个端点的鉴权该怎么做？
@claude 修一下用户面板里那个 TypeError
```

### 两种模式

- **交互模式**：workflow 里**不给** `prompt` 输入。Claude 等待触发词（默认 `@claude`），进展和结果发在触发它的 issue / PR 评论里。
- **自动模式**：workflow 里**给了** `prompt` 输入。不等提及，直接跑，默认结果写在 workflow run 日志里，除非 prompt 让它去发评论且它有能发评论的工具。

### 谁能触发

两道检查，任一不过就失败：

- **写权限**：issue 和 PR 事件上，触发者必须有仓库写权限。要放行没有写权限的特定用户，设 `allowed_non_write_users` 并传自己的 `github_token`。
- **必须是人**：机器人触发一律拒绝，除非列进 `allowed_bots`。这是为了防止机器人把 Claude 拉进死循环。定时任务也走这一检查——GitHub 会把定时运行归到某个仓库用户名下（通常是最后改 cron 的人）。

### 定时跑

```yaml
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"
jobs:
  report:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: read
      id-token: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "总结昨天的提交和当前的 open issues"
          claude_args: |
            --model claude-opus-5
            --allowedTools "mcp__github__list_commits,mcp__github__list_issues"
```

⚠️ **纯文本 prompt 的自动模式下，Claude 默认没有任何 shell 或 GitHub API 权限**，你必须用 `claude_args` 里的 `--allowedTools` 或 `settings` 输入里的 `permissions.allow` 规则显式授权。如果你调用的是 Skill，那 Skill 自己的 `allowed-tools` 前置元数据会生效。

> GitHub 只从默认分支运行定时 workflow；公开仓库里，60 天没有仓库活动就会自动停用定时任务。

### 控成本

每次运行烧两种资源：GitHub Actions 分钟数 + token。降低办法：

- `@claude` 请求写具体，减少来回轮次
- 用 issue 模板把上下文一次给足
- CLAUDE.md 保持精简（每次运行都读）
- `claude_args` 里设 `--max-turns` 限制轮次
- 设 workflow 级超时
- 用 GitHub 的 concurrency 控制限制并行

### 常见问题

**@claude 没反应**：确认 App 装了、workflow 开着、secret 配了、评论里 `@claude` 是完整单词（不是 `/claude` 或 `@claude-bot`）、评论者有写权限。

**Claude 的提交不触发 CI**：GitHub 不会为用默认 `GITHUB_TOKEN` 创建的提交触发 workflow。如果你传了 `github_token: ${{ secrets.GITHUB_TOKEN }}`，把它删掉，让它以 Claude GitHub App 身份认证。

## 3.11 上下文管理

| 命令 | 什么时候用 |
| --- | --- |
| `/clear` | 换任务了。**这是最该养成的习惯。** |
| `/compact` | 当前任务还没做完但上下文快满了，手动压缩一次 |
| `/context` | 想知道上下文被什么占满了，以及哪些 memory 文件生效了 |

**压缩后什么会保留？** 项目根目录的 CLAUDE.md 会被重新从磁盘读回来注入。子目录里的 CLAUDE.md 和带 `paths` 的规则会在 Claude 再次读到匹配文件时重新加载。**只在对话里说过的话不会保留。**

这条机制推导出一条非常实用的纪律：**任何你希望在长任务里一直生效的约束，都不能只在对话里说，必须写进 CLAUDE.md。**

---

# 第四篇：标准工作流

工具讲完了，这一篇讲怎么用。**大部分人用不好 Claude Code，不是因为不知道有哪些功能，而是因为把它当搜索引擎用——一次问一句，拿到答案就走。**

## 4.1 从需求到交付的五步链路

```
探索 → 计划 → 实现 → 验证 → 交付
```

每一步都有明确的产出物和明确的失败信号。

### 第一步：探索

**目标**：让 Claude 建立起对相关代码的理解，让你确认它理解对了。

```text
在动手之前，先看一下这个项目里用户注册是怎么走的。
从入口路由开始，把涉及的文件和它们的职责列出来。先不要改任何东西。
```

**产出物**：一份文件清单 + 数据流描述。

**失败信号**：它开始猜测。看到"通常这类项目会……"、"一般来说……"这种措辞，说明它没找到真东西。这时候要给更具体的线索，或者切到 `plan` 模式再来一次。

**省时技巧**：如果这一步要扫的文件很多，用 Subagent（3.5）。让 explorer 去扫，只把清单带回来。

### 第二步：计划

**目标**：拿到一份你能审的方案，而不是一堆已经写好的代码。

```bash
claude --permission-mode plan
```

或者会话里 `Shift+Tab` 切到 plan 模式。plan 模式下 Claude 只能读，不能改，直到你批准方案。

```text
基于刚才的理解，给我一个加"邮箱验证"功能的方案。
说清楚：要改哪些文件、每个文件改什么、需要新增哪些文件、
数据库要不要动、有哪些你不确定的地方。
```

**产出物**：一份分步方案。

**这一步是整个流程里投入产出比最高的。** 五分钟审方案，能省掉半小时审一个方向就错了的 diff。

**审方案时重点看三件事**：

1. 它有没有漏掉你知道但没说的约束？（漏了就补进 CLAUDE.md，而不是只在对话里说）
2. 它列的"不确定的地方"你能不能现在就回答掉？
3. 改动范围是不是超出了你的预期？超出了就明确划界。

### 第三步：实现

**目标**：让它写代码，你不要在中途打断微观决策。

```text
按这个方案实现。每完成一个文件停一下告诉我，我要看着走。
```

或者放手：

```text
按这个方案实现，全部做完再告诉我。
```

**两种模式的选择**：改动局限在你熟悉的代码里 → 放手；碰到你不熟或者风险高的地方 → 分步。

**中途要不要打断？** 如果它走偏了，`Esc` 打断，说清楚哪里偏了。**不要用"不对，重来"** ——它会丢掉已经做对的部分。用"第 2 步做错了，X 应该是 Y，其他保留"。

### 第四步：验证

**这是最容易被跳过、也最不该跳过的一步。**

```text
跑测试和 lint，把真实输出贴给我。
```

注意措辞：**"把真实输出贴给我"**。不加这句，它可能会说"测试通过了"而没真跑。

更进一步，用独立上下文来验收（3.5 里的 verifier Subagent）：

```text
@agent-verifier 验证一下刚才的改动
```

独立上下文的价值在于它没有"这是我写的代码"的自我确认偏误。

**验证清单**：

- [ ] 测试跑了，输出贴出来了
- [ ] Lint / typecheck 过了
- [ ] 改动真的解决了原始问题（不是绕过了它）
- [ ] 没有引入新的依赖（除非你批准过）
- [ ] 边界情况：空输入、超长输入、并发、失败重试

### 第五步：交付

```text
把改动提交，commit message 按项目的 Conventional Commits 约定写。
然后 push 到一个新分支并开 PR，PR 描述里说清楚改了什么、为什么、怎么验证的。
```

**交付之后还有一步**：如果这次会话里有任何"我又解释了一遍"的时刻，把那条解释写进 CLAUDE.md。这是让下一次更省力的唯一办法。

## 4.2 提示词模板库

以下模板可以直接存成 Skill（3.4），变成 `/命令`。

### 理解陌生代码

```text
我要改 <功能>。在动手之前：
1. 找到相关的入口点
2. 画出从入口到数据落库的调用链
3. 列出这条链路上任何看起来不寻常的地方（自定义逻辑、注释里的警告、绕过标准做法的写法）
先不要改任何东西。
```

### 定位 Bug

```text
现象：<具体描述，包含实际输入和实际输出>
期望：<期望输出>
复现步骤：<步骤>

先找到根因再改。找到之后先告诉我根因是什么，我确认后你再动手。
不要在没有确认根因的情况下"试着修一下"。
```

最后一句很重要。没有它，模型的默认倾向是快速给出一个看起来合理的修改。

### 重构

```text
重构 <目标>，约束：
- 外部行为完全不变，现有测试必须全绿
- 不新增依赖
- 一次只做一类改动，先做 <A>，做完让我看，再做 <B>

开始前先告诉我你打算怎么拆这几步。
```

### 写测试

```text
给 <模块> 补测试。要求：
- 覆盖正常路径、边界情况、错误路径
- 用项目现有的测试工具和风格（先看一下 tests/ 下已有的写法）
- 不要为了覆盖率写没有意义的断言
写完把测试跑一遍，贴输出。
```

### 代码审查

```text
审查我在这个分支上的改动（跟 main 对比）。重点看：
1. 正确性 bug —— 给出具体的触发条件和会出什么错
2. 能复用现有代码但重复实现了的地方
3. 明显的性能问题

每条问题给出 文件:行号。不确定的标注"不确定"。
不要提风格问题，lint 会管。
```

### 让它写文档

```text
给 <模块> 写文档，读者是刚加入的同事。
要包含：它解决什么问题、怎么用（可运行的例子）、有哪些坑。
不要写"这个函数返回一个字符串"这种从签名就能看出来的东西。
```

## 4.3 反模式清单

这些是实践中最常见、代价也最大的错误用法。

### ❌ 一个会话干所有事

从改 bug 聊到重构再聊到写文档。上下文被无关内容填满，压缩后早期的关键约定丢失，模型开始犯低级错误。

**改法**：一个任务一个会话，`/clear` 是你最好的朋友。

### ❌ 把约定只在对话里说

"记住我们这个项目不用 lodash" —— 说了，当场生效了，压缩之后没了。

**改法**：写进 CLAUDE.md。判断标准：这条约定下次会话还需要吗？需要就写进去。

### ❌ 不看方案直接批准

plan 模式给了方案，扫一眼觉得"差不多"就批了。然后花二十分钟 review 一个方向就错了的 diff。

**改法**：审方案的时间应该和审 diff 的时间相当。方案错了，后面全白做。

### ❌ 相信"测试通过了"这句话

**改法**：永远要求"把真实输出贴出来"。

### ❌ 在没有 Git 保护的情况下放手让它干

**改法**：动手前先 commit 或者建分支。`git stash` 也行。有了 Git 兜底，你才敢用 `auto` 模式。

### ❌ 用模糊的纠正

"不对"、"这样不行"、"重新弄一下"。模型不知道哪里不对，会随机改一个方向，经常把对的部分也一起改掉。

**改法**：具体到哪一步、哪个文件、哪个判断错了，以及正确的是什么。

### ❌ 让它读整个目录

"把 `src/` 全部读一遍然后告诉我架构是怎样的"。这会瞬间烧掉大量上下文，而且效果比 grep 差。

**改法**：让它先用 Glob/Grep 缩小范围，或者扔给 Subagent。

### ❌ 在陌生仓库里直接用 auto 模式

别人的仓库里可能有 `.claude/skills/` 带着宽松的 `allowed-tools`，也可能有 `.mcp.json` 指向不知道什么服务。

**改法**：clone 之后先看 `.claude/` 目录和 `.mcp.json` 里有什么，再决定用什么权限模式。

### ❌ 把 API key 写进配置文件然后提交

**改法**：`.mcp.json` 里用 `${VAR}` 环境变量展开；GitHub Actions 里用 secrets。

## 4.4 一条实用的自检

每次会话结束前问自己三个问题：

1. **这次有没有哪句话我上次也说过？** → 写进 CLAUDE.md。
2. **这次有没有哪套流程我以后还会走一遍？** → 做成 Skill。
3. **这次有没有哪件事本来就不该让模型自己决定？** → 写成 Hook。

坚持一个月，你的 `.claude/` 目录会变成整个项目最有价值的资产之一。

---

# 第五篇：实战案例库

五个案例，从易到难。建议每个都真的跑一遍，光看是学不会的。

## 案例一：三十分钟读懂一个陌生仓库

**场景**：你接手了一个别人写的项目，或者想给一个开源项目提 PR。

**第一步：让它自己摸底**

```bash
cd the-unfamiliar-repo
claude --permission-mode plan
```

```text
我第一次看这个项目。请按顺序回答：
1. 它是做什么的？（读 README 和 package.json / pyproject.toml 之类）
2. 怎么跑起来？怎么跑测试？
3. 目录结构里每个顶层目录的职责
4. 主要的数据流：请求进来之后经过哪些层
5. 有没有明显不寻常的地方（自定义框架、绕过标准做法的写法、注释里的警告）

先不要改任何东西。
```

**第二步：验证它的理解**

不要直接信。挑一个它的结论去验证：

```text
你说鉴权在 middleware/auth.py 里做。把那个文件的关键部分贴出来，
指出具体是哪几行完成了鉴权。
```

如果它贴不出来或者贴的东西对不上，说明前面的结论是猜的。

**第三步：固化成 CLAUDE.md**

```text
基于上面的理解，跑 /init 生成一份 CLAUDE.md。
重点放在：构建/测试命令、目录职责、你发现的不寻常之处。
不要写从代码里一眼能看出来的东西。
```

**第四步：找一个小切口练手**

```text
在这个项目里找一个小的、低风险的改进点：
一个缺失的错误处理、一个没覆盖的边界情况、一处明显的重复代码。
列出候选，说明每个的风险等级。
```

从最低风险的那个开始做，走一遍完整的五步链路。这样你既熟悉了代码，也验证了自己的构建/测试环境是通的。

## 案例二：给一个脚本加上生产级的健壮性

**场景**：本仓库的 `crawler.py` 是一个典型的"能跑但不健壮"的脚本——直接 `requests.get`，直接 `data['current_weather']['temperature']`，没有超时、没有重试、没有错误处理。API 抖动一次，定时任务就红一次。

这是最能体现 Claude Code 价值的场景：**改动小、边界多、容易漏。**

**提示词**：

```text
读一下 crawler.py。这个脚本每天由 GitHub Actions 跑一次，
目前任何网络抖动或 API 返回格式变化都会让它直接崩掉。

给它加上生产级的健壮性：
1. HTTP 请求加超时
2. 失败重试，指数退避，最多 3 次
3. 校验响应结构，缺字段时给出清晰的错误信息而不是 KeyError
4. 结构化的日志输出，让 Actions 日志里能看出发生了什么
5. 失败时以非零退出码结束，这样 Actions 才会标红

约束：
- 只用标准库和已有依赖（requests、pandas），不要新增依赖
- 保持现有的 CSV 输出格式和文件名不变
- 保留现有的中文注释风格

先给我方案，我确认后再动手。
```

**为什么这么写：**

- **说清楚运行环境**（"每天由 GitHub Actions 跑一次"）—— 这决定了错误处理的策略是重试而不是弹窗。
- **逐条列出要求** —— 比"让它更健壮"具体得多。
- **明确约束** —— 不加依赖、不改输出格式。没有这两条，它很可能给你引入 `tenacity` 和 `structlog`。
- **先要方案** —— 你能在写代码前就发现方向问题。

**验收**：

```text
现在验证：
1. 正常路径还能跑通吗？跑一次，贴输出。
2. 把 URL 改成一个不存在的域名，确认重试逻辑生效、最终以非零码退出。
   验证完把 URL 改回来。
3. 确认 weather_data.csv 的格式和之前完全一致。
```

第 2 条是关键。**健壮性代码最容易出的问题就是"错误路径从来没被跑过"。**

## 案例三：搭一条每日自动数据管道

**场景**：这正是本仓库在做的事——每天定时抓数据、存进 CSV、提交回仓库。

**完整提示词**：

```text
我要做一条每日自动数据管道，需求：

- 每天北京时间早上 7 点，从 <数据源> 抓一次数据
- 追加到 data/<name>.csv，字段：<字段列表>
- 用 GitHub Actions 跑，跑完把新数据提交回仓库
- 失败时 Actions 要标红，日志里能看出失败原因

现有的 crawler.py 和 .github/workflows/daily_task.yml 是同类实现，
可以参考它们的风格。

给我方案：需要新增/修改哪些文件、cron 表达式怎么写、
Actions 需要什么权限、有哪些容易踩的坑。
```

**这个案例里的几个真实坑，值得提前问清楚：**

| 坑 | 说明 |
| --- | --- |
| **cron 用 UTC** | GitHub Actions 的 cron 是 UTC 时间。北京时间早 7 点 = UTC 前一天 23 点，写成 `0 23 * * *` |
| **定时任务不准时** | GitHub 的定时任务在高峰期会延迟，甚至跳过。不要依赖它做精确到分钟的事 |
| **需要 `contents: write`** | 不给这个权限，机器人推不回去 |
| **空提交会失败** | 数据没变化时 `git commit` 会返回非零码让整个 job 红。要处理这种情况 |
| **公开仓库 60 天休眠** | 公开仓库连续 60 天没有活动，定时任务会被自动停用 |
| **并发写冲突** | 如果同时有别的 workflow 也在推，需要 `git pull --rebase` 或 concurrency 控制 |

把这些直接写进提示词，或者更好——写进 CLAUDE.md，让每次涉及 Actions 的会话都自动知道。

**加一层 Claude 自己的审查**：

数据管道最怕的是"跑成功了但数据是错的"。可以再挂一个定时 workflow，让 Claude 每周检查一次数据质量：

```yaml
name: Weekly Data Check
on:
  schedule:
    - cron: "0 1 * * 1"   # 每周一 UTC 01:00
  workflow_dispatch:
jobs:
  check:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
      id-token: write
    steps:
      - uses: actions/checkout@v6
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            检查 weather_data.csv 的数据质量：
            1. 有没有缺失的日期（应该每天一条）
            2. 有没有明显异常的值（温度超出合理范围、风速为负）
            3. 有没有重复行
            如果发现问题，用 GitHub MCP 工具开一个 issue 说明；没问题就什么都不做。
          claude_args: |
            --allowedTools "Read,Bash(python3 *),mcp__github__issue_write"
```

> 注意 `--allowedTools` 里必须显式列出它需要的工具。自动模式下不授权就什么都干不了。

## 案例四：把一份 Markdown 变成可部署的网站

**场景**：你写了一份长文档，想让它有个能直接访问的网页版。**这个案例的产物就是你正在读的这个网站。**

**架构**：

```
Claude红皮书.md              ← 唯一的内容来源
tools/build_site.py          ← 构建脚本：Markdown → HTML
docs/
  index.html                 ← 构建产物
  assets/site.css            ← 手写样式
  assets/site.js             ← 目录高亮、阅读进度
  favicon.svg
.github/workflows/pages.yml  ← 构建 + 部署
```

**为什么是这个架构：**

- **内容和呈现分离。** 改内容只动 `.md`，改样式只动 `.css`，两者互不干扰。
- **构建产物入库。** `docs/index.html` 是提交进仓库的，这样 GitHub Pages 的"从分支部署"模式也能直接用，不强依赖 Actions。
- **CSS/JS 手写不生成。** 让脚本去生成样式表是自找麻烦；样式是要反复微调的东西，应该能直接改。

**提示词**：

```text
我有一份长 Markdown 文档，想做成一个能部署到 GitHub Pages 的静态站点。要求：

- 单页，左侧固定目录，右侧正文
- 目录跟随滚动高亮当前章节
- 顶部有阅读进度条
- 支持深色模式（跟随系统）
- 移动端要能正常读：目录折到上面，宽表格能横向滚动
- 用 Python 构建，只依赖 markdown 库
- 输出到 docs/，这样 Pages 的"从分支部署"和 Actions 部署两种方式都能用

先给我文件结构和构建脚本的设计，我确认后再写。
```

**几个容易被忽略的细节**（值得直接写进提示词）：

1. **中文标题的锚点。** Markdown 转 HTML 时中文标题生成的 id 需要 URL 编码，目录链接和标题 id 必须用同一套规则。用 `markdown` 库的 `toc` 扩展可以保证一致。
2. **宽表格。** 技术文档里表格很多，不套一层 `overflow-x: auto` 的容器，移动端整个页面会被撑横。
3. **`.nojekyll`。** GitHub Pages 默认走 Jekyll，会忽略下划线开头的文件。放一个空的 `.nojekyll` 文件在输出目录里省心。
4. **深色模式下的代码块。** 亮色下好看的深色代码块，在深色模式下可能和背景糊在一起，要单独给一个更深的值。

## 案例五：写一个属于你的 Skill

**场景**：你发现自己第三次在粘同一段说明了。

**从对话到 Skill 的最短路径：**

```text
把我们刚才走的这套流程做成一个 Skill，放在项目的 .claude/skills/ 下。

流程是：<用两三句话复述刚才做了什么>

要求：
- 只有我能手动调用，你不要自动触发（这个流程有副作用）
- 需要用到 git 命令，预授权掉，不要每次都问我
- 接收一个参数：<参数说明>
```

**一个真实可用的例子：发版前检查**

`.claude/skills/preflight/SKILL.md`：

```markdown
---
name: preflight
description: 发版前的完整检查清单。合并到主分支或打 tag 之前运行。
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(npm *) Read Grep Glob
argument-hint: [目标分支，默认 main]
---

## 当前状态

分支：!`git rev-parse --abbrev-ref HEAD`

未提交改动：
!`git status --short`

与目标分支的差异：
!`git diff --stat $1...HEAD 2>/dev/null || git diff --stat main...HEAD`

## 检查清单

依次执行并报告每一项的真实结果，任何一项失败就停下来告诉我：

1. 工作区是干净的（上面的 git status 为空）
2. `npm run lint` 通过
3. `npm run typecheck` 通过
4. `npm test` 通过——贴出真实输出，不要只说"通过了"
5. 上面的 diff 里没有：调试用的 console.log、被注释掉的代码块、
   TODO/FIXME 标记、硬编码的 URL 或密钥
6. 如果 diff 里改了公开 API，确认 README 或文档也同步更新了

全部通过后，给我一份适合放进 release notes 的改动摘要。
```

这个 Skill 用到了本书讲过的四个机制：

- **动态上下文注入**（`` !`command` ``）—— Claude 拿到的是真实的 git 状态
- **`disable-model-invocation`** —— 发版检查有副作用，不能让它自己决定什么时候跑
- **`allowed-tools`** —— 预授权 git 和 npm，不然每条命令都要点确认
- **`$1` 位置参数** —— `/preflight develop` 就能对比 develop 分支

**Skill 写完之后的验证**：

```text
用 /preflight 跑一次，然后告诉我：
1. 动态注入的 git 命令输出是不是真的进来了
2. 有没有哪一步弹了权限确认（不该弹的话说明 allowed-tools 没配对）
```

---

# 附录

## 附录 A：Claude API 快速上手

如果你要把 Claude 嵌进自己的应用，而不是在终端里用它写代码，那就是 API 的场景。

### 安装与认证

```bash
pip install anthropic
```

```python
import anthropic

# 默认从环境解析凭证：ANTHROPIC_API_KEY，或 ANTHROPIC_AUTH_TOKEN，
# 或 `ant auth login` 建立的 profile。不要把 key 硬编码进代码。
client = anthropic.Anthropic()
```

> `ANTHROPIC_API_KEY` 没设 **不等于** 没有凭证。SDK 的解析顺序是：`ANTHROPIC_API_KEY` → `ANTHROPIC_AUTH_TOKEN` → `ant auth login` 的活跃 profile → Workload Identity Federation → 磁盘上的默认 profile。跑 `ant auth status` 能看到当前生效的是哪个。

### 最基础的一次调用

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,
    messages=[{"role": "user", "content": "法国的首都是哪里？"}],
)

# response.content 是内容块列表（TextBlock、ThinkingBlock、ToolUseBlock…）
# 访问 .text 之前先检查 .type
for block in response.content:
    if block.type == "text":
        print(block.text)
```

### 几个必须知道的参数

**`max_tokens`**：别给小了，撞到上限会把输出从中间截断。非流式请求默认给 `16000` 左右（避免撞 HTTP 超时），流式可以给到 `64000`。分类这种确定短输出的场景才降到几百。

**思考（thinking）**：当代模型用自适应思考，直接：

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,
    thinking={"type": "adaptive", "display": "summarized"},
    output_config={"effort": "high"},   # low | medium | high | xhigh | max
    messages=[{"role": "user", "content": "..."}],
)
```

⚠️ **常见的过时写法**：`thinking={"type": "enabled", "budget_tokens": N}`。这在 Opus 5、Opus 4.8/4.7、Sonnet 5、Fable 5 系列上会直接返回 **400**。`budget_tokens` 只在 Opus 4.6 / Sonnet 4.6 上作为过渡手段还能用，新代码不要写。

⚠️ **`display` 的默认值变了**：在 Opus 5、Opus 4.8/4.7、Sonnet 5、Fable 5 上默认是 `"omitted"`（思考块文本为空）。如果你要把推理过程展示给用户，必须显式写 `display: "summarized"`，否则界面上看起来就是长时间无响应。

**流式**：任何可能长输入、长输出、或 `max_tokens` 给得高的请求都应该流式，避免撞 HTTP 超时：

```python
with client.messages.stream(
    model="claude-opus-5",
    max_tokens=64000,
    messages=[{"role": "user", "content": "..."}],
) as stream:
    message = stream.get_final_message()
```

### Prompt 缓存：最重要的省钱手段

缓存是**前缀匹配**的。渲染顺序是 `tools` → `system` → `messages`。前缀里任何一个字节变了，后面全部失效。

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,
    cache_control={"type": "ephemeral"},   # 自动缓存最后一个可缓存块
    system=large_document_text,
    messages=[{"role": "user", "content": "总结要点"}],
)
```

**验证缓存是否命中**：

```python
print(response.usage.cache_creation_input_tokens)  # 写入缓存的 token（约 1.25 倍成本）
print(response.usage.cache_read_input_tokens)      # 命中缓存的 token（约 0.1 倍成本）
print(response.usage.input_tokens)                 # 未缓存的 token（全价）
```

如果重复请求下 `cache_read_input_tokens` 一直是 0，说明有东西在悄悄让缓存失效。最常见的三个元凶：

1. system prompt 里有 `datetime.now()` 或 UUID
2. `json.dumps()` 没排序，字典顺序在变
3. 工具列表顺序不稳定

**设计原则**：稳定内容放前面（固定的 system prompt、确定顺序的工具列表），易变内容放最后一个缓存断点之后（时间戳、每次请求的 ID、用户的问题）。

### 工具调用

```python
tools = [{
    "name": "get_weather",
    "description": "查询指定城市的当前天气",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
        "additionalProperties": False,
    },
    "strict": True,   # 保证 tool_use.input 严格符合 schema
}]
```

**两个必须知道的规则**：

1. **并行工具调用**：一条 assistant 消息里可能有多个 `tool_use` 块。执行完之后，所有的 `tool_result` 必须放在**同一条** user 消息里返回。拆成多条会悄悄训练模型不再做并行调用。
2. **失败的工具也要返回**：用 `tool_result` 加 `is_error: true`，不要直接丢掉。

**不想手写循环**的话，SDK 提供了 Tool Runner：Python 用 `@beta_tool` 装饰器 + `client.beta.messages.tool_runner(...)`，TypeScript 用 `betaZodTool` + `client.beta.messages.toolRunner(...)`。

### 错误处理

不要用一个宽泛的 `except` 兜住所有东西——那会丢掉"可重试"和"不可重试"的区别：

```python
try:
    response = client.messages.create(...)
except anthropic.NotFoundError:
    ...                              # 模型 ID 或端点错了，不要重试
except anthropic.RateLimitError as e:
    retry_after = int(e.response.headers.get("retry-after", "60"))
except anthropic.APIStatusError as e:
    if e.status_code >= 500:
        ...                          # 服务端错误，可重试
    else:
        ...                          # 4xx，不要重试
except anthropic.APIConnectionError:
    ...                              # 网络问题，可重试
```

> SDK 自带重试（默认 2 次，覆盖 408/409/429/5xx 和连接错误）。只有需要超出这个行为时才自己写重试逻辑。

### 其他常用能力

| 能力 | 关键点 |
| --- | --- |
| **批处理** | `client.messages.batches.create(...)`，异步跑，**5 折**。结果顺序是乱的，必须按 `custom_id` 取，不能按位置取 |
| **PDF 输入** | `{"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": ...}}`，放在文本块**之前** |
| **Files API** | `client.files.upload(...)` 拿到 `file_id`，多次请求复用同一个文件 |
| **引用** | 在 document 块上设 `citations: {enabled: true}`，响应会拆成多个 text 块，被引用的块带 `citations` 数组 |
| **结构化输出** | 用 `output_config: {format: {...}}`。旧的 `output_format` 参数已废弃 |
| **Token 计数** | `client.messages.count_tokens(...)`。**不要用 tiktoken**，那是别家的分词器 |
| **网页搜索** | 服务端工具，`{"type": "web_search_20260209", "name": "web_search"}` |

### 几个高频踩坑

⚠️ **Assistant prefill 已被移除**。在 Fable 5/5.1、Opus 5、Sonnet 5 和 4.6/4.7/4.8 全家族上，最后一条 assistant 消息做 prefill 会返回 400。想控制输出格式，用结构化输出或 system prompt 指令。

⚠️ **模型 ID 不要加日期后缀**。表格里的 ID 就是完整的：写 `claude-sonnet-5`，不要写 `claude-sonnet-5-20251114`。

⚠️ **工具入参必须用 `json.loads()` 解析**，不要对序列化后的字符串做原始匹配。新模型的 JSON 转义方式（Unicode、斜杠）可能和你预期的不同。

⚠️ **服务端工具的错误不会抛异常**。网页搜索、网页抓取出错时返回 HTTP 200，结果块的 `content` 是一个错误对象而不是列表。索引之前先判断类型。

## 附录 B：速查表

### 权限模式

| 模式 | 配置值 | 一句话 |
| --- | --- | --- |
| Manual | `default` | 只读，其他都问 |
| Accept Edits | `acceptEdits` | 改文件不问，跑命令要问 |
| Plan | `plan` | 只读 + 出方案，批准前不动手 |
| Auto | `auto` | 分类器代替你审，长任务用 |
| Don't Ask | `dontAsk` | 只有白名单里的工具能用，CI 用 |
| Bypass | `bypassPermissions` | 全放行，**只在容器里用** |

### 配置文件位置

```
~/.claude/settings.json              个人设置 + Hooks
~/.claude/CLAUDE.md                  个人偏好
~/.claude/skills/<name>/SKILL.md     个人 Skill
~/.claude/agents/<name>.md           个人 Subagent
~/.claude/rules/*.md                 个人规则
~/.claude/projects/<p>/memory/       自动记忆（本机）

./CLAUDE.md                          项目记忆（入库）
./CLAUDE.local.md                    个人的项目偏好（gitignore）
./.claude/rules/*.md                 项目规则（入库）
./.claude/settings.json              项目设置 + Hooks（入库）
./.claude/settings.local.json        本地覆盖（不入库）
./.claude/skills/<name>/SKILL.md     项目 Skill（入库）
./.claude/agents/<name>.md           项目 Subagent（入库）
./.mcp.json                          项目 MCP 服务器（入库）
```

### 该用哪个机制

| 症状 | 用 |
| --- | --- |
| "它又忘了我们不用 X" | CLAUDE.md |
| "改前端时才需要的那套规范" | `.claude/rules/` + `paths` |
| "这套流程我每周走三次" | Skill |
| "这个调查会把上下文塞满" | Subagent |
| "这件事必须每次都做" | Hook |
| "我要让它查数据库/Jira" | MCP |
| "全组都要用这套配置" | Plugin |

### Skill 前置元数据

```yaml
---
name: my-skill
description: 做什么 + 什么时候用（关键场景写最前面）
when_to_use: 补充触发场景
argument-hint: [参数提示]
disable-model-invocation: true    # 只有我能调（有副作用的操作）
user-invocable: false             # 只有 Claude 能调（背景知识）
allowed-tools: Bash(git *) Read   # 本轮免授权
disallowed-tools: WebFetch        # 本轮禁用
model: opus
effort: xhigh
context: fork                     # 在 Subagent 里跑
paths: ["src/**/*.ts"]            # 限制自动触发范围
---
```

### Subagent 前置元数据

```yaml
---
name: my-agent
description: 什么时候委派给它（写 "use proactively" 提高自动调用率）
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet                     # opus | sonnet | haiku | fable | 完整 ID
permissionMode: acceptEdits
maxTurns: 20
skills: [security-checklist]
memory: project
effort: low
isolation: worktree
---
```

### 环境变量

| 变量 | 作用 |
| --- | --- |
| `ANTHROPIC_API_KEY` | API key，会让 Claude Code 跳过订阅登录 |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Subagent 的默认模型 |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` | 关闭自动记忆 |
| `CLAUDE_CODE_NEW_INIT=1` | 开启交互式 `/init` |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` | 加载 `--add-dir` 目录里的 CLAUDE.md |
| `CLAUDE_CODE_SYNC_SKILLS=1` | 同步 claude.ai 账号上启用的 Skill（需配合 `-p`） |

## 附录 C：常见问题

**Q：CLAUDE.md 写了但它不遵守。**

CLAUDE.md 是作为 system prompt 之后的一条 user 消息注入的，Claude 会读会尽量遵守，但**没有强制保证**，指令越模糊越容易被忽略。排查顺序：

1. 跑 `/context`，看 **Memory files** 里有没有你的文件。没有就是根本没加载。
2. 确认文件位置对（见 3.1 的加载表）。
3. 把指令写得更具体（"用 2 空格缩进" 优于 "格式化好"）。
4. 找冲突指令——多个 CLAUDE.md 说了相反的话，它可能随机挑一条。
5. 如果这件事**必须**在某个时刻发生，改成 Hook。CLAUDE.md 管不了这个。

`InstructionsLoaded` Hook 可以打印出到底加载了哪些指令文件、什么时候加载的，是调试路径规则和懒加载的利器。

**Q：CLAUDE.md 太大了怎么办？**

超过 200 行会占更多上下文且降低遵守度（超过 4 MiB 会被直接跳过）。办法：

- 用带 `paths` 的规则，只在改到相关文件时才加载
- 删掉能从代码里推导出来的内容（目录结构、依赖列表、架构概览）
- 保留推导不出来的（坑、理由、和工具默认行为不同的约定）
- `/doctor` 会主动给出精简建议

注意：拆成 `@path` import **不省上下文**，import 的文件启动时一样全量加载。

**Q：`/compact` 之后指令好像丢了。**

项目根目录的 CLAUDE.md 会在压缩后重新从磁盘读回来。子目录的 CLAUDE.md 和带 `paths:` 的规则会在 Claude 再次读到匹配文件时重新加载。**只在对话里说过的话不会回来。**

**Q：Skill 触发不了 / 触发太频繁。**

- 触发不了：`description` 写得不够。把最关键的使用场景放最前面（`description` + `when_to_use` 合并后会被截断到 1536 字符），加上触发短语。
- 触发太频繁：加 `paths` 限制范围，或者设 `disable-model-invocation: true` 改成手动调用。

**Q：为什么我明明有订阅，却在扣 API 的钱？**

检查 `ANTHROPIC_API_KEY` 环境变量。设了这个变量，Claude Code 会跳过订阅登录直接用 key 计费。

**Q：GitHub Actions 里 @claude 没反应。**

按顺序查：App 装了吗 → workflow 开着吗 → secret 配了吗 → 评论里是完整的 `@claude` 吗（不是 `/claude` 或 `@claude-bot`）→ 评论的人有仓库写权限吗。

**Q：Claude 推的提交不触发 CI。**

GitHub 不会为用默认 `GITHUB_TOKEN` 创建的提交触发 workflow。如果你在 action 里传了 `github_token: ${{ secrets.GITHUB_TOKEN }}`，删掉它，让它以 Claude GitHub App 的身份认证；或者传一个自定义 App 的 token。

**Q：在别人的仓库里用 Claude Code 安全吗？**

要看之后再用。两个具体风险点：

- `.claude/skills/` 里的 `allowed-tools` **不受工作区信任限制**，一个仓库里的 Skill 可以给自己授予很宽的工具权限。
- `.mcp.json` 里的服务器虽然需要你确认信任，但确认之后它就能读你的数据、发你的请求。

clone 之后先看这两处，再决定用什么权限模式。

**Q：Subagent 和 Skill 到底怎么选？**

问一句：**这件事会产生大量你不想留在主上下文里的中间信息吗？**

- 会 → Subagent（扫 200 个文件、跑一堆探索性命令）
- 不会 → Skill（一套固定的操作步骤）

也可以组合：Skill 里设 `context: fork`，就是在 Subagent 里跑的 Skill。

---

## 结语

这本书讲的所有机制，最终都指向同一件事：**把你脑子里的项目知识，变成机器可读的形式，留在仓库里。**

CLAUDE.md 是你的项目常识，Skill 是你的操作手册，Hook 是你的红线，Subagent 是你的分工，MCP 是你的外部接口。它们加起来构成的 `.claude/` 目录，本质上是一份**给 AI 协作者的入职文档**——而它恰好对人类新同事也一样有用。

从今天开始，每次会话结束前问自己一遍第 4.4 节的三个问题。一个月之后回头看，你会发现改变的不只是 AI 的输出质量，还有你自己对项目的理解深度。

---

**License**：本项目采用 MIT License 开源。

**贡献**：欢迎提 issue 和 PR 补充内容、纠正错误。Claude 更新很快，任何一处过时的描述都值得被指出来。
