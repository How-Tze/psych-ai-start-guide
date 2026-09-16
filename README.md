# 心理学研究者的 AI Start Guide

《心理学研究的 AI 进阶手册》动态配套入门站。

## 核心逻辑

**产品界面 → API → Harness → Workflow**

这不是能力等级表。读者先完成一个真实任务，只有在出现新的摩擦时才升级工具：反复搬背景、来源太多、需要搜索、需要批量、需要代码执行、需要跨文件工作。

## 首版目标

- 主导航按“研究者现在想做什么”组织；
- 同时覆盖国际与中国大陆主流 AI 产品生态；
- 单独解释 API：是什么、为什么用、怎么计费、怎么配置；
- 提供 DeepSeek API → 沉浸式翻译、BYOK 客户端、最小研究脚本等渐进示例；
- 产品页和价格信息全部带核查日期；
- 产品页采用统一的“五问”结构，不写成厂商说明书；
- HTML 是持续维护的主版本，PDF 以后只作为阶段性快照。

## 当前阅读主线

`现在就开始 → 普通聊天 → Project / Workspace → 来源型论文阅读 → Deep Research → API → Code Agent → Work Agent`

每一步都强调“什么时候继续停留”和“什么时候值得升级”。

## 目录

- `chapters/`：读者任务主线
- `products/`：动态产品页
- `appendices/`：公开附录
- `data/`：产品/API Provider 的动态结构化信息
- `examples/`：教学示例
- `field-tests/`：内部实测记录，不作为读者主导航
- `docs/`：版本、编辑规则和主手册后续备忘

## 当前教学实例

- `examples/api-batch/`：合成开放式回答 × DeepSeek API 的最小、可恢复批量脚本。
- `docs/handbook-v1.2-backlog.qmd`：留待主手册下一版讨论的“AI × 开放科学”备忘。

## 本地预览

安装 Quarto 后：

```bash
quarto preview
```

正式发布计划使用 GitHub Pages。上线前才写入真实的 `site-url` / `repo-url`，当前本地预览不会渲染无效的占位网址。

Windows 第一次本地预览的详细步骤见：`docs/FIRST_RENDER_WINDOWS.md`。
