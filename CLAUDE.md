# CLAUDE.md

给 Claude Code 看的项目说明。改动本仓库前先读这份文件。

## 这是什么

一条跑在 GitHub Actions 上的每日数据管道：定时抓取东京实时天气 → 追加写入 `weather_data.csv` → 由机器人提交回 `main`。没有服务器、没有数据库、没有构建产物。

`docs/` 与数据管道无关，是《Claude 红皮书》迁走后留下的跳转页。

## 仓库结构

```text
.
├── crawler.py                      # 全部抓取逻辑，单文件顺序脚本，无函数封装
├── weather_data.csv                # 数据产物，由 Actions 追加，人工不要编辑
├── .github/workflows/
│   ├── daily_task.yml              # 每日抓取 + 提交（cron '34 22 * * *'，UTC）
│   └── pages.yml                   # docs/ 变更时发布 GitHub Pages
├── docs/index.html                 # 旧链接跳转页
└── README.md
```

## 本地运行

```bash
pip install requests pandas
python crawler.py
```

会在当前目录创建或追加 `weather_data.csv`。**本地跑一次会真的写一行数据**，验证完记得 `git checkout weather_data.csv`，别把调试数据混进提交。

仓库没有 `requirements.txt`，依赖直接写在 `daily_task.yml` 的 `pip install requests pandas` 这一步里。新增依赖要同时改工作流和 README 的本地运行说明。

## 没有测试和 lint

仓库里没有测试套件、没有 linter、没有 CI 检查脚本。改完 `crawler.py` 的验证方式就是本地跑一次看输出，或在 Actions 页面用 `workflow_dispatch` 手动触发。

## 约定

- 注释和文档一律中文，`crawler.py` 里的注释风格是逐步骤讲解，面向教学读者，不要精简掉。
- 工作流的 `name` 和 step 名称也是中文。
- 数据提交由 `github-actions[bot]` 完成，提交信息固定为 `🤖 自动更新天气数据`，不要改。

## 已知坑

- **cron 走 UTC**：`'34 22 * * *'` 对应北京时间次日 06:34。改时间先做时区换算。Actions 定时任务在高峰期会被延迟甚至跳过，别指望分钟级准时。
- **公开仓库连续 60 天无活动，定时任务会被自动停用**，需要手动去 Actions 页面重新启用。
- **`weather_data.csv` 的 Date 列格式不统一**：最早两行是 `2026-05-07T11:00`（接口原始格式），之后是 `2026-05-07 11:00:00`。解析历史数据时要兼容两种。
- `daily_task.yml` 的提交步骤用 `git commit ... || exit 0`，没有新数据时静默成功，不会让流水线变红。
- `crawler.py` 没有任何错误处理：接口超时或返回结构变化会直接抛异常让流水线失败。这是刻意的（失败要看得见），修 bug 时别顺手包一层 `try/except` 把失败吞掉。

## 换城市 / 换数据源

改 `crawler.py` 里 `url` 的 `latitude` / `longitude` / `timezone`，然后同步改提取字段和写 CSV 的部分，以及 README 对应说明。

## docs/ 目录

《Claude 红皮书》已迁到 <https://github.com/FuzzyLogic112/claude-red-book>（在线阅读 <https://fuzzylogic112.github.io/claude-red-book/>）。`docs/index.html` 只是跳转页，别往里加正文内容。动 `docs/` 会触发 `pages.yml` 重新部署。
