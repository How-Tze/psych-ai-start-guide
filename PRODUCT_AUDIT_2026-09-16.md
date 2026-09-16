# 核心产品第一轮官方资料审计

**核查日期：2026-09-16**  
**阶段：Phase 1A — 官方能力审计**  
**目的：** 先回答“这个产品当前官方上能做什么”，暂不把注册、支付、地区网络、真实额度等体验性问题混进事实层。

## 1. 第一轮结论

当前 8 个核心生态全部值得保留，但它们在 Start Guide 中承担的教学角色不同：

| 生态 | 在 Start Guide 中的主要角色 | 第一轮判断 |
|---|---|---|
| ChatGPT | 通用入口：Chat → Projects → Deep Research → Codex / Work | 核心 |
| Claude | Projects / Research / Claude Code / Cowork | 核心 |
| Gemini / Gemini Notebook | Deep Research + 以来源为中心的 notebook | 核心 |
| DeepSeek | 国内 API + 第三方 Harness + DeepSeek Harness | 核心 |
| Kimi | 国内 Deep Research / Work Agent / Kimi Code | 核心 |
| Qwen | 国内 Deep Research / API / 开源 Qwen Code | 核心 |
| GLM | API + Coding Plan + 第三方 Harness 后端 | 核心但角色更窄 |
| 腾讯 WorkBuddy | 国内桌面 Work Agent / 本地文件 / 项目空间 | 核心 |

## 2. 一个重要的结构性发现

产品页不能再只用“有没有某功能”的二元表格。至少需要区分：

1. **原生产品能力**：例如 ChatGPT Projects、Claude Cowork、Kimi Deep Research；
2. **模型/API 能力**：例如 DeepSeek API、GLM API；
3. **可接入的 Harness**：例如 DeepSeek → Claude Code / OpenCode，GLM Coding Plan → Claude Code / Cursor；
4. **计费通道**：网页订阅、按量 API、Coding Plan / Token Plan 等可能完全不同。

这将直接影响后续产品卡和 API 章节设计。

## 3. 暂不下结论的字段

以下字段不能只靠官方宣传页确认，需要第二轮“现实可用性实测”：

- 中国大陆网络环境是否可直接访问；
- 注册是否需要特定手机号/地区；
- 国内银行卡、支付宝、微信、境外卡分别能否支付；
- 免费账户是否足以完成本册指定教程；
- API 充值最低金额、余额有效期、发票等现实问题；
- 桌面端在 Windows / macOS 的实际安装门槛；
- Agent 对本地文件、终端、浏览器的真实授权流程。

这些项目将由“官网核查 + 用户实际操作”共同完成，不从模型知识推断。

## 4. 第二轮建议的实测顺序

按中国读者的启动价值排序：

1. DeepSeek：网页/API/Key/充值/第三方 Harness；
2. Kimi：普通对话/Deep Research/Kimi Code/Work；
3. Qwen：Qwen Studio/Deep Research/Qwen Code/百炼 API；
4. GLM：开放平台 API/Coding Plan/Claude Code 接入；
5. WorkBuddy：安装/本地文件权限/深度调研/模型切换；
6. ChatGPT；
7. Claude；
8. Gemini / Gemini Notebook。

国际产品的功能事实已经比较清楚；现实访问与支付部分对中国大陆读者更需要谨慎核验。

## 5. 下一工作单元

下一步不再扩产品数量，进入两个并行任务：

- **Phase 1B：现实可用性实测**：逐个完成注册、免费路径、支付、安装与权限检查；
- **Phase 2：第一条完整教程**：优先完成 `DeepSeek API → 第三方工具 → 第一次成功调用`，再分支到沉浸式翻译、BYOK 客户端和最小脚本。

在线发布环境（GitHub / GitHub Pages / Quarto）暂时不需要用户搭建；等首批可阅读内容达到可预览状态后再建立，避免现在先维护一个空站点。
