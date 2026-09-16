# PROJECT STATUS

**阶段：** v0.10 / Phase 2C — 本地 HTML render-ready

**最近核查：** 2026-09-16

## 已冻结的内容逻辑

1. 产品界面 → API → Harness → Workflow 四层认知链；
2. 任务为主导航，产品为第二导航；
3. 国际与中国 AI 产品并列；
4. 核心生态：ChatGPT、Claude、Gemini / Gemini Notebook、DeepSeek、Kimi、Qwen、GLM、腾讯 WorkBuddy；
5. API 是正式主线；
6. HTML 为动态正式版本，PDF 后续作为版本快照；
7. Start Guide 不写成产品说明书，只保留会改变选择、理解、安全和科研工作流的信息；
8. 遇到摩擦再升级，不把产品层级写成能力等级。

## v0.10 本轮完成

- 修正 `_quarto.yml` 中 API / Agent / 安全章节的旧编号，导航与当前文件结构一致；
- 加入公开 render 白名单：正式网站只构建 26 个读者页面；
- 从公共侧栏移除 field test、审计 schema、编辑规则、主手册 backlog 等内部维护页；
- 清理 DeepSeek 公共产品页中的内部 field-test 链接与“下一轮审计”工作痕迹；
- 上线前不再写 `<YOUR_GITHUB_USERNAME>` 一类占位 URL，避免本地 HTML 出现无效 GitHub 链接；
- 加入 `lang: zh-CN` 与第一轮响应式 CSS 微调；
- 新增 `.gitignore`，排除 `_site/`、Quarto 缓存、API Key / `.env`、Python 缓存；
- 新增 `docs/FIRST_RENDER_WINDOWS.md`：Windows 第一次真实 Quarto 预览步骤；
- 新增 `docs/GITHUB_PAGES_SETUP.md`：本地 render 通过后的 GitHub Pages 上线路线；
- 使用 Pandoc 对全部 26 个公开页面做结构性预渲染：页面可解析，内部 HTML 链接 0 个缺失；
- YAML 预检通过，教学 Python 脚本此前已通过语法检查。

## 当前限制

当前执行环境没有可用的 Quarto CLI，且无法在沙箱内取得其发行二进制，因此**尚未声称真实 Quarto render 通过**。Pandoc 预渲染只用于提前发现结构和链接错误，不能替代 Quarto 对 Mermaid、搜索、导航和 callout 的最终渲染。

## 用户下一步

在 Windows 本地安装 Quarto 稳定版，然后：

```powershell
quarto preview
```

视觉检查通过后运行：

```powershell
quarto render
```

重点检查：首页、任务选择图、第一次 API 配置、API 最小研究脚本、DeepSeek 产品页、API 工具附录。

## render 通过后的下一阶段

Phase 2D：

1. 根据真实 Quarto HTML 做一次轻量 CSS 调整；
2. 创建 GitHub 仓库；
3. 写入真实 `site-url` / `repo-url`；
4. 首次执行 `quarto publish gh-pages`；
5. 再启用 GitHub Actions 自动发布；
6. 发布第一次公开预览 URL。
