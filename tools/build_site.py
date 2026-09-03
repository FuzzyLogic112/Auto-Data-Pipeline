#!/usr/bin/env python3
"""把 Claude红皮书.md 编译成 docs/ 下可直接部署到 GitHub Pages 的静态站点。

用法：
    pip install markdown
    python tools/build_site.py

产物：docs/index.html（docs/assets/ 下的 CSS/JS 是手写的，本脚本不覆盖）。
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

try:
    import markdown
    from markdown.extensions.toc import slugify_unicode
except ImportError:  # pragma: no cover - 只在缺依赖时触发
    sys.exit("缺少依赖，请先执行：pip install markdown")

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "Claude红皮书.md"
OUT_DIR = ROOT / "docs"
OUT_FILE = OUT_DIR / "index.html"

SITE_TITLE = "Claude 红皮书：从安装到实战的全链路使用指南"
SITE_DESC = "写给开发者和 AI 工具重度用户的 Claude、Claude Code 与 Claude API 非官方中文指南。"
REPO_URL = "https://github.com/FuzzyLogic112/Auto-Data-Pipeline"
SOURCE_URL = f"{REPO_URL}/blob/main/Claude%E7%BA%A2%E7%9A%AE%E4%B9%A6.md"

# hero 右侧信息卡，改这里即可
META = [
    ("版本", "v0.1.0"),
    ("最后校验", "2026-09-03"),
    ("内容范围", "认知 · 安装 · 核心能力 · 工作流 · 实战"),
]


def render_markdown(text: str) -> tuple[str, list[dict]]:
    """返回 (正文 HTML, toc_tokens)。"""
    md = markdown.Markdown(
        extensions=["extra", "toc", "sane_lists", "admonition"],
        extension_configs={
            # 默认的 slugify 会把非 ASCII 全部丢掉，"3.3 自动记忆" 会变成锚点 "#33"。
            # 用 slugify_unicode 保留中文，锚点才是可读、可分享的。
            # permalink 关掉：中文标题里挂个 ¶ 反而碍眼。
            "toc": {
                "anchorlink": False,
                "permalink": False,
                "slugify": slugify_unicode,
            },
        },
    )
    body = md.convert(text)
    return body, md.toc_tokens


def flatten_toc(tokens: list[dict]) -> list[tuple[int, str, str]]:
    """把 toc_tokens 摊平成 (level, id, 文本)。只取 h1/h2 两层进侧边栏。

    正文第一个 H1 是书名，页面上已经作为文章标题显示了，不重复进目录——
    但它下面的 H2（阅读入口等）要保留。
    """
    out: list[tuple[int, str, str]] = []

    def walk(nodes: list[dict], level: int, skip_self: bool = False) -> None:
        for i, node in enumerate(nodes):
            is_title = skip_self and i == 0
            if level <= 2 and not is_title:
                out.append((level, node["id"], node["name"]))
            if level < 2:
                walk(node.get("children", []), level + 1)

    walk(tokens, 1, skip_self=True)
    return out


def build_toc_html(entries: list[tuple[int, str, str]]) -> str:
    lines = []
    for level, anchor, name in entries:
        cls = "toc-link" if level == 1 else "toc-link toc-link--sub"
        lines.append(
            f'<a class="{cls}" href="#{html.escape(anchor, quote=True)}">'
            f"{html.escape(name)}</a>"
        )
    return "\n".join(lines)


def wrap_tables(body: str) -> str:
    """宽表格在窄屏上会把整页撑横，套一层可横向滚动的容器。"""
    return re.sub(
        r"<table>(.*?)</table>",
        lambda m: f'<div class="table-scroll"><table>{m.group(1)}</table></div>',
        body,
        flags=re.DOTALL,
    )


def build_page(body: str, toc_html: str) -> str:
    meta_html = "\n".join(
        f"          <div><span class=\"panel-label\">{html.escape(k)}</span>"
        f"<strong>{html.escape(v)}</strong></div>"
        for k, v in META
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(SITE_TITLE)}</title>
  <meta name="description" content="{html.escape(SITE_DESC, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(SITE_TITLE, quote=True)}">
  <meta property="og:description" content="{html.escape(SITE_DESC, quote=True)}">
  <meta name="theme-color" content="#c15f3c">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/site.css">
  <script defer src="assets/site.js"></script>
</head>
<body>
  <div class="progress" aria-hidden="true"><span></span></div>

  <header class="topbar">
    <a class="brand" href="#top" aria-label="返回顶部">
      <span class="brand-mark">C</span>
      <span>Claude 红皮书</span>
    </a>
    <nav class="topnav" aria-label="主导航">
      <a href="#online-book">在线阅读</a>
      <a href="#toc">目录</a>
      <a class="cta" href="{SOURCE_URL}" target="_blank" rel="noopener">Markdown 原稿</a>
    </nav>
  </header>

  <main id="top">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-copy">
        <p class="eyebrow">非官方开源指南 · 持续更新版</p>
        <h1 id="hero-title">Claude 红皮书</h1>
        <p class="hero-lede">从安装、配置、核心能力到实战案例，系统梳理 Claude Code、CLAUDE.md、Skills、Subagents、Hooks、MCP 与 Claude API 的完整用法。</p>
        <div class="hero-actions">
          <a class="button button-primary" href="#online-book">开始阅读</a>
          <a class="button button-secondary" href="{REPO_URL}" target="_blank" rel="noopener">在 GitHub 上查看</a>
        </div>
      </div>
      <aside class="hero-panel" aria-label="版本信息">
{meta_html}
      </aside>
    </section>

    <section class="book-shell" id="online-book">
      <details class="toc-panel" id="toc" open>
        <summary class="toc-heading">目录</summary>
        <nav class="toc-list" aria-label="文章目录">
{toc_html}
        </nav>
      </details>

      <article class="book-content">
{body}
      </article>
    </section>
  </main>

  <footer class="site-footer">
    <p>本站由 <a href="{SOURCE_URL}" target="_blank" rel="noopener">Claude红皮书.md</a>
    经 <code>tools/build_site.py</code> 生成，部署在 GitHub Pages。内容为非官方整理，请以
    <a href="https://code.claude.com/docs" target="_blank" rel="noopener">Claude Code 官方文档</a> 为准。</p>
  </footer>

  <button class="back-top" data-back-top type="button" aria-label="回到顶部">↑</button>
</body>
</html>
"""


def main() -> None:
    if not SOURCE.exists():
        sys.exit(f"找不到正文文件：{SOURCE}")

    text = SOURCE.read_text(encoding="utf-8")
    body, toc_tokens = render_markdown(text)
    body = wrap_tables(body)
    toc_html = build_toc_html(flatten_toc(toc_tokens))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(build_page(body, toc_html), encoding="utf-8")

    print(f"✅ 已生成 {OUT_FILE.relative_to(ROOT)}"
          f"（{OUT_FILE.stat().st_size / 1024:.1f} KB，目录 {toc_html.count('<a ')} 条）")


if __name__ == "__main__":
    main()
