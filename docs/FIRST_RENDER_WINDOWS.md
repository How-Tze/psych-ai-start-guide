# 第一次本地 HTML 预览：Windows 操作流程

**适用阶段：** Start Guide v0.10 以后，第一次用 Quarto 看真实网站效果。  
**核查日期：** 2026-09-16

## 1. 安装 Quarto

1. 打开 Quarto 官方下载页：https://quarto.org/docs/download/ 。
2. 选择 **Release** 版本，不需要安装 Pre-release。2026-09-16 官方页面列出的稳定版为 1.10.18。
3. Windows 选择 `.msi` 安装包，按默认选项安装即可。
4. 安装完成后，关闭并重新打开 PowerShell。
5. 输入：

```powershell
quarto --version
```

能返回版本号即可。

> 不需要为了这个项目额外安装 R、RStudio 或 Jupyter。当前网站正文没有需要执行的 R/Python 代码块；示例 Python 脚本只是供读者下载和手动运行。

## 2. 解压项目

建议把项目放在一个以后可以长期维护的位置，例如：

```text
C:\Users\你的用户名\Documents\Research_Projects\psych-ai-start-guide
```

不要直接在压缩包内部运行 Quarto。

确认根目录至少能看到：

```text
_quarto.yml
index.qmd
chapters\
products\
assets\
```

## 3. 打开 PowerShell 到项目目录

最简单的方法：

1. 在资源管理器打开项目文件夹；
2. 点击地址栏；
3. 输入 `powershell`；
4. 回车。

或者手动：

```powershell
cd "C:\Users\你的用户名\Documents\Research_Projects\psych-ai-start-guide"
```

## 4. 第一次预览

运行：

```powershell
quarto preview
```

Quarto 会启动本地预览服务器，并通常自动打开浏览器。网址一般类似：

```text
http://localhost:xxxx/
```

保持这个 PowerShell 窗口打开。修改 `.qmd` 或 CSS 后，预览会自动重建或刷新。

## 5. 这次只检查六件事

不要开始重新写正文。第一次真实 HTML 预览只做视觉和导航检查：

1. **导航**：顶部导航和左侧目录是否能正常跳转；
2. **Mermaid**：API 批量脚本页的数据流图是否正常显示；
3. **表格**：桌面端是否过宽，手机宽度是否可以横向查看；
4. **Callout**：提示、警告框是否清楚但不过度抢眼；
5. **代码块**：PowerShell / Python / text 示例是否可读，复制按钮是否正常；
6. **移动端**：把浏览器窗口缩窄到手机宽度，检查正文、表格和导航。

建议重点打开：

```text
/
/chapters/01-task-map.html
/chapters/07-api-first-setup.html
/chapters/09-api-research-script.html
/products/deepseek.html
/appendices/api-tools.html
```

## 6. 正式构建检查

预览没有明显问题后，停止 `quarto preview`（PowerShell 中按 `Ctrl + C`），再运行：

```powershell
quarto render
```

如果成功，根目录会生成：

```text
_site\
```

这个目录是生成的网站，不是以后主要编辑的源文件。项目已经在 `.gitignore` 中忽略 `_site/`。

## 7. 如果报错，记录什么

只需要保存：

- PowerShell 中从 `ERROR` 开始到错误结尾的文字；
- 报错涉及的文件名和行号；
- Quarto 版本号（`quarto --version`）。

不要把 API Key、`.env`、账号信息或私人文件路径中的敏感内容公开出去。

## 8. 这一步之后

本地 `quarto render` 通过后，再建立 GitHub 仓库和 GitHub Pages。上线前会补入真实的 `site-url` 与 `repo-url`；当前 `_quarto.yml` 有意不写占位网址，避免把无效链接渲染进预览站。
