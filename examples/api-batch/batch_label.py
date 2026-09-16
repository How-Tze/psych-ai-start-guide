"""Minimal, resumable DeepSeek API batch example for the Start Guide.

Teaching purpose only. The labels and synthetic responses are not a validated
psychological coding scheme.
"""

from __future__ import annotations

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
INPUT_CSV = HERE / "input_responses.csv"
OUTPUT_DIR = HERE / "output"
OUTPUT_JSONL = OUTPUT_DIR / "results.jsonl"
RUN_METADATA_JSON = OUTPUT_DIR / "run_metadata.json"

API_URL = os.getenv(
    "DEEPSEEK_API_URL",
    "https://api.deepseek.com/chat/completions",
)
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")
API_KEY = os.getenv("DEEPSEEK_API_KEY")
PROMPT_VERSION = "theme-label-demo-v1"

SYSTEM_PROMPT = """你正在执行一个教学用的候选主题标记任务。
只能从以下标签中选择一个或多个：
academic_pressure, rumination, sleep_habits, social_stress, other

要求：
1. 只根据提供的文本判断，不补充背景信息。
2. 如果前四类都不合适，使用 other。
3. 返回严格 JSON，不要添加 Markdown：
{"labels": ["label"], "reason": "一句简短理由"}

这只是候选标记，不代表经过验证的心理学编码。
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_completed_ids(path: Path) -> set[str]:
    completed: set[str] = set()
    if not path.exists():
        return completed
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("status") == "ok" and record.get("id"):
                completed.add(str(record["id"]))
    return completed


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def call_model(response_text: str) -> tuple[dict, str | None]:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": response_text},
        ],
    }

    r = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    content = data["choices"][0]["message"]["content"]
    returned_model = data.get("model")
    return {"raw": content, "full_response": data}, returned_model


def parse_json_if_possible(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def main() -> None:
    if not API_KEY:
        raise SystemExit(
            "Missing DEEPSEEK_API_KEY. Set it in your current terminal session first."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not RUN_METADATA_JSON.exists():
        RUN_METADATA_JSON.write_text(
            json.dumps(
                {
                    "created_utc": utc_now(),
                    "api_url": API_URL,
                    "model_requested": MODEL,
                    "prompt_version": PROMPT_VERSION,
                    "system_prompt": SYSTEM_PROMPT,
                    "input_file": INPUT_CSV.name,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    completed = load_completed_ids(OUTPUT_JSONL)

    with INPUT_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        item_id = row["id"]
        text = row["response"]

        if item_id in completed:
            print(f"SKIP {item_id}: already completed")
            continue

        base = {
            "id": item_id,
            "response": text,
            "model_requested": MODEL,
            "timestamp_utc": utc_now(),
            "prompt_version": PROMPT_VERSION,
        }

        try:
            result, returned_model = call_model(text)
            raw = result["raw"]
            record = {
                **base,
                "status": "ok",
                "model_returned": returned_model,
                "raw_model_output": raw,
                "parsed_output": parse_json_if_possible(raw),
                # Keep the full provider response locally for audit/debugging.
                "provider_response": result["full_response"],
                "error": None,
            }
            print(f"OK   {item_id}")
        except Exception as exc:  # teaching example: preserve failure and continue
            record = {
                **base,
                "status": "error",
                "model_returned": None,
                "raw_model_output": None,
                "parsed_output": None,
                "provider_response": None,
                "error": f"{type(exc).__name__}: {exc}",
            }
            print(f"ERR  {item_id}: {exc}")

        append_jsonl(OUTPUT_JSONL, record)

    print(f"\nResults: {OUTPUT_JSONL}")


if __name__ == "__main__":
    main()
