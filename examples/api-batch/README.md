# 合成文本 API 批处理教学

输入八条虚构回答；标签只是演示，不是有效心理学测量。要求 Python 3.10+。在本目录打开终端。

## 先离线检查

```powershell
python batch_label.py --dry-run
python -m unittest -v
```

两条命令不请求 API、不需要 Key。安装实际调用依赖：`python -m pip install -r requirements.txt`。Windows 若 python 不可用而已安装 Python，可试 py。

## 小规模实际调用

在当前会话中用不回显的方式输入自己的 Key，或使用已有安全环境配置。不要把真实 Key 写进命令历史、脚本、文档或仓库。

PowerShell：

```powershell
$demoSecureKey = Read-Host "DeepSeek API Key" -AsSecureString
$env:DEEPSEEK_API_KEY = [System.Net.NetworkCredential]::new("", $demoSecureKey).Password
python batch_label.py --max-calls 2
Remove-Item Env:DEEPSEEK_API_KEY
```

重新设置 Key 后再次运行会跳过相同批次中格式通过的记录；提高 --max-calls 才会在一次运行发出更多请求。DEEPSEEK_MODEL 可选择官方当前支持的模型。端点固定为官方 DeepSeek，避免把 Key 发往不明地址。不得同时在同一 output 目录运行两个进程。

## 怎样理解产物

- output/results.jsonl：追加保留成功、失败和格式错误。format_ok 仅表示 JSON、标签和理由格式合格，不是科学正确。
- 每次运行独立的 UUID.json：输入摘要、完整提示、模型及参数。
- output/runs.jsonl：每次运行的调用、跳过、格式成功和错误计数。
- 输入、模型、提示或参数改变会形成新批次，保守地重新处理整份输入；不会覆盖旧结果。
- 原始响应保留在本地；异常只记录类型，避免把 Key 带入错误信息。
- 输出被截断、JSON 或标签无效时可重跑；没有自动重试。超时可能已经产生服务端费用，重跑可能再次收费。
- max-calls 是请求数量上限，不是金额封顶。单次输出上限也不能保证精确账单，先查控制台实际用量。
- 若进程被强制终止，确认没有运行中的进程后才能手动移除 output/.running；不要直接删除整个 output。
- 本例是单用户教学脚本，没有服务端幂等或大规模生产调度承诺。

仓库版本将 output/ 列入忽略规则；若手动下载文件到自己的 Git 项目，也应在该项目的 .gitignore 中加入 output/。练习内容可公开，真实输入与完整响应不得未经审查发布。此版本只做离线模拟测试，没有声称已发起付费 API 调用。

请求参数依据：2026-10-13 核对 [DeepSeek Chat Completions API](https://api-docs.deepseek.com/api/create-chat-completion/)。本例关闭思考模式、启用 JSON 输出、限制最多 1024 输出 tokens，并继续自行校验标签结构；这些选项一并写入运行元数据。格式模式仍不能保证标签含义正确。
