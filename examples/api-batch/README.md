# API Batch Teaching Example

This directory supports the Start Guide chapter “API 真正对研究者有用的地方：一个最小批量脚本”.

The survey responses are **fully synthetic** and the theme labels are **teaching-only**, not a validated psychological coding scheme.

## Run

Install:

```bash
python -m pip install -r requirements.txt
```

PowerShell session-only key:

```powershell
$env:DEEPSEEK_API_KEY="your-key"
python batch_label.py
```

macOS / Linux:

```bash
export DEEPSEEK_API_KEY='your-key'
python batch_label.py
```

Optional environment variables:

- `DEEPSEEK_MODEL`
- `DEEPSEEK_API_URL`

## Output

Generated files go to `output/`, which is ignored by Git by default. The script writes `run_metadata.json` once to record the requested model, API URL and prompt version, then appends item-level records to `results.jsonl`. Review and redact any real research outputs before deciding whether they belong in an open repository.
