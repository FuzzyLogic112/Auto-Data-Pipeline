# Claude 红皮书

> 一本写给开发者、独立开发者和 AI 工具重度用户的 Claude、Claude Code 与 Claude API 非官方开源中文指南。

**[📖 在线阅读](https://fuzzylogic112.github.io/Auto-Data-Pipeline/)** · [Markdown 原稿](./Claude红皮书.md)

## 这是什么

《Claude 红皮书》围绕 Claude Code 的真实使用场景整理，目标是帮你把 AI 编码代理真正放进日常工作和软件项目里，而不是停留在"问一句答一句"。

它不是 Anthropic 官方文档，也不代表官方产品承诺。内容基于公开文档、实际界面和实战经验整理，适合作为上手路线、工作流参考和案例材料阅读。

## 内容包括

- **基础认知**：Claude 应用 / Claude Code / Claude API 三个入口的区别，模型家族与选型，和 Cursor、Copilot 的差异。
- **安装与配置**：各平台安装方式、认证、权限模式、命令速查、配置文件都在哪。
- **核心能力**：CLAUDE.md 项目记忆、`.claude/rules/` 路径规则、自动记忆、Skills、Subagents、Hooks、MCP、Plugins、Git 与 GitHub 工作流、GitHub Actions、上下文管理。
- **标准工作流**：探索 → 计划 → 实现 → 验证 → 交付的完整链路，提示词模板库，反模式清单。
- **实战案例**：读懂陌生仓库、给脚本加健壮性、搭每日数据管道、把 Markdown 变成网站、写自己的 Skill。
- **附录**：Claude API 快速上手、配置速查表、常见问题。

## 仓库结构

```text
.
├── Claude红皮书.md              # 完整正文，唯一的内容来源
├── tools/
│   └── build_site.py            # 构建脚本：Markdown → docs/index.html
├── docs/                        # GitHub Pages 站点（构建产物 + 手写样式）
│   ├── index.html               # 由 build_site.py 生成，不要手改
│   ├── assets/site.css          # 手写样式，可直接改
│   ├── assets/site.js           # 目录高亮、阅读进度、窄屏折叠目录
│   ├── favicon.svg
│   └── .nojekyll                # 让 Pages 跳过 Jekyll 处理
├── .github/workflows/
│   ├── pages.yml                # 构建并部署到 GitHub Pages
│   └── daily_task.yml           # 每日天气数据抓取（见下）
├── crawler.py                   # 天气数据抓取脚本
└── weather_data.csv             # 抓取结果
```

> 这个仓库同时还是一条每日自动数据管道的示例（`crawler.py` + `daily_task.yml`），书里的[实战案例二和案例三](https://fuzzylogic112.github.io/Auto-Data-Pipeline/#案例二给一个脚本加上生产级的健壮性)就以它为素材。两部分互不影响。

## 本地构建

```bash
pip install markdown
python tools/build_site.py
```

产物写到 `docs/index.html`。直接用浏览器打开就能预览，或起一个本地服务器：

```bash
python -m http.server -d docs 8000
# 打开 http://localhost:8000
```

**改内容**只动 `Claude红皮书.md`，然后重新构建；**改样式**只动 `docs/assets/site.css`，构建脚本不会覆盖它。

## 部署到 GitHub Pages

两种方式任选其一，仓库对两种都做好了准备。

### 方式一：GitHub Actions（推荐）

1. 打开仓库的 **[Settings → Pages](https://github.com/FuzzyLogic112/Auto-Data-Pipeline/settings/pages)**。
2. **Source** 选 **GitHub Actions**。这一步只需做一次。
3. 把改动推到 `main` 分支，或在 **Actions** 页面手动点 **Run workflow**。

`.github/workflows/pages.yml` 会重新从 Markdown 构建并部署。

> 第 2 步没法用工作流代劳：`actions/configure-pages` 的 `enablement: true` 需要
> `GITHUB_TOKEN` 去调建站点的 API，而该调用会被拒绝（`Resource not accessible by
> integration`）。所以首次启用必须手点一次。

### 方式二：从分支部署（不用 Actions）

1. 先在本地跑一次 `python tools/build_site.py`，把 `docs/` 的改动提交上去。
2. **Settings → Pages** → **Source** 选 **Deploy from a branch**。
3. 分支选 `main`，目录选 **`/docs`**，保存。

这种方式部署的是仓库里已提交的 `docs/index.html`，所以每次改完正文都**必须记得重新构建并提交**。Actions 工作流在检测到不同步时会给出警告。

部署完成后访问：**https://fuzzylogic112.github.io/Auto-Data-Pipeline/**

> 首次启用 Pages 后可能要等一两分钟才能访问到。

## 说明

Claude 更新很快，安装方式、模型名称、额度、入口位置和命令参数都可能变化。涉及具体功能、价格和账号能力时，请以 [Claude Code 官方文档](https://code.claude.com/docs)、[Claude 平台文档](https://platform.claude.com) 和你账号实际显示为准。

发现过时或错误的内容，欢迎提 issue 或 PR。

## License

本项目采用 [MIT License](./LICENSE) 开源。
