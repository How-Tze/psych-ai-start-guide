# GitHub Pages 首次上线流程（待本地 render 通过后执行）

**状态：** 预备说明，不属于公开网站正文。  
**核查日期：** 2026-09-16

Quarto 官方当前支持三种 GitHub Pages 路线：把渲染结果提交到 `docs/`、本地执行 `quarto publish gh-pages`、或用 GitHub Actions 自动发布。本项目计划采用 **源代码留在 `main` + 生成网站发布到 `gh-pages`** 的方式。

正式上线时按以下顺序操作：

1. 在 GitHub 新建公开仓库，建议仓库名：`psych-ai-start-guide`；
2. 把项目源文件提交到 `main`，不要提交 `_site/`、`.env`、API Key；
3. 把 `_quarto.yml` 中的 `site-url` 和 `repo-url` 改成真实用户名和仓库地址；
4. 在本地项目目录运行一次：

```powershell
quarto publish gh-pages
```

Quarto 会首次创建并推送 `gh-pages` 分支；对于普通项目站点，GitHub 通常会自动识别该分支作为 Pages 来源。

5. 网站正常上线后，再加入自动发布 workflow。官方当前推荐的核心配置为：

```yaml
on:
  workflow_dispatch:
  push:
    branches: main

name: Quarto Publish

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Check out repository
        uses: actions/checkout@v7
      - name: Set up Quarto
        uses: quarto-dev/quarto-actions/setup@v2
      - name: Render and Publish
        uses: quarto-dev/quarto-actions/publish@v2
        with:
          target: gh-pages
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

6. GitHub 仓库中进入 `Settings → Actions → General → Workflow permissions`，确认 Actions 具有 **Read and write permissions**。

正式执行这一阶段时，应再按当日 GitHub / Quarto 页面复核一次按钮名称和发布方式。
