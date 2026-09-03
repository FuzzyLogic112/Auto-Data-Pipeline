# Auto-Data-Pipeline

一条跑在 GitHub Actions 上的每日自动数据管道：定时抓取东京实时天气，追加到 CSV，再把结果提交回仓库。不需要服务器，不需要数据库，全靠 GitHub 免费的定时任务跑。

## 它做什么

每天北京时间 06:34（UTC 22:34），GitHub Actions 会：

1. 拉取仓库代码，装好 Python 环境和依赖
2. 执行 `crawler.py`，从 [Open-Meteo](https://open-meteo.com/) 免费接口抓一次东京当前天气
3. 把时间、温度、风速追加写入 `weather_data.csv`
4. 以机器人身份把新数据提交回 `main` 分支

于是 `weather_data.csv` 会自己一天天长起来，形成一份连续的时间序列。

## 仓库结构

```text
.
├── crawler.py                      # 抓取脚本：请求接口、解析字段、追加写 CSV
├── weather_data.csv                # 抓取结果，由 Actions 自动追加
├── .github/workflows/
│   ├── daily_task.yml              # 每日定时抓取并提交
│   └── pages.yml                   # 发布 docs/ 下的迁移跳转页
└── docs/index.html                 # 《Claude 红皮书》迁移跳转页（见下）
```

## 本地运行

```bash
pip install requests pandas
python crawler.py
```

会在当前目录生成或追加 `weather_data.csv`。

## 换一个城市 / 换一套数据

`crawler.py` 里的接口地址决定了抓什么：

```python
url = "https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&current_weather=true&timezone=Asia/Tokyo"
```

- 换城市：改 `latitude` / `longitude`，并把 `timezone` 改成对应时区（例如北京是 `Asia/Shanghai`）
- 换字段：Open-Meteo 支持 `hourly`、`daily` 等参数，改完接口后同步改脚本里提取字段和写 CSV 的部分

## 改抓取时间

编辑 `.github/workflows/daily_task.yml` 里的 cron 表达式：

```yaml
on:
  schedule:
    - cron: '34 22 * * *'   # UTC 时间，对应北京时间次日 06:34
```

⚠️ GitHub Actions 的 cron 走 **UTC**，写之前先做时区换算。另外定时任务在高峰期会被延迟甚至跳过，不要依赖它做精确到分钟的事；公开仓库连续 60 天没有活动，定时任务会被自动停用。

## 关于 docs/ 目录

这个仓库曾经托管过《Claude 红皮书》，后来迁到了独立仓库。`docs/index.html` 现在只是一个跳转页，让已经传播出去的旧链接不至于直接 404。

- 新仓库：**https://github.com/FuzzyLogic112/claude-red-book**
- 在线阅读：**https://fuzzylogic112.github.io/claude-red-book/**

书里的实战案例二、案例三仍然以本仓库的 `crawler.py` 和 `daily_task.yml` 为素材。

## License

本项目采用 [MIT License](./LICENSE) 开源。
