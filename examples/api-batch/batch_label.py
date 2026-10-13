"""Synthetic teaching example; format checks do not validate psychological coding."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

HERE = Path(__file__).resolve().parent
API_URL = "https://api.deepseek.com/chat/completions"
REQUEST_OPTIONS = {"thinking": {"type": "disabled"},
                   "response_format": {"type": "json_object"}}
LABELS = {"academic_pressure", "rumination", "sleep_habits", "social_stress", "other"}
SYSTEM_PROMPT = """你在执行合成教学文本的候选标记。只使用提供的文本。
只从 academic_pressure, rumination, sleep_habits, social_stress, other 选择标签。
other 只在其余标签均不适用时单独使用。返回 JSON 对象：
{"labels":["label"],"reason":"简短理由"}
不要 Markdown，不补写信息。这不是已验证的心理学编码。"""


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False,
                                    sort_keys=True).encode("utf-8")).hexdigest()


def validate_output(raw):
    value = json.loads(raw)
    if not isinstance(value, dict) or set(value) != {"labels", "reason"}:
        raise ValueError("Expected exactly labels and reason")
    labels = value["labels"]
    if not isinstance(labels, list) or not labels:
        raise ValueError("labels must be a nonempty list")
    if any(not isinstance(x, str) or x not in LABELS for x in labels):
        raise ValueError("Unknown label")
    if len(set(labels)) != len(labels) or ("other" in labels and len(labels) != 1):
        raise ValueError("Duplicate or contradictory labels")
    if not isinstance(value["reason"], str) or not value["reason"].strip():
        raise ValueError("reason must be nonempty text")
    return value


def read_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != ["id", "response"]:
            raise ValueError("Input columns must be id,response")
        rows = list(reader)
    ids = [r["id"] for r in rows]
    if not rows or len(set(ids)) != len(ids):
        raise ValueError("Input must be nonempty and ids unique")
    if any(set(r) != {"id", "response"} or
           not all(isinstance(v, str) and v.strip() for v in r.values())
           for r in rows):
        raise ValueError("Input cells must be nonempty text")
    return rows


def append_record(path, record):
    # Keep a torn final line as evidence; terminate it before adding a new record.
    if path.exists() and path.stat().st_size:
        with path.open("rb") as stream:
            stream.seek(-1, 2)
            needs_newline = stream.read(1) != b"\n"
        if needs_newline:
            with path.open("ab") as stream:
                stream.write(b"\n")
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")


def completed_keys(path):
    completed = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
                if record.get("status") == "format_ok":
                    validate_output(record["raw_model_output"])
                    completed.add(record["request_key"])
            except (ValueError, KeyError, TypeError, AttributeError):
                continue
    return completed


@contextmanager
def run_lock(output):
    lock = output / ".running"
    try:
        handle = lock.open("x", encoding="utf-8")
    except FileExistsError:
        raise RuntimeError("Another run or stale .running lock exists; see README.") from None
    try:
        with handle:
            handle.write(str(os.getpid()))
        yield
    finally:
        lock.unlink()


def call_model(text, config):
    import requests
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise RuntimeError("Missing DEEPSEEK_API_KEY")
    response = requests.post(API_URL, headers={"Authorization": "Bearer " + key},
                             json={**REQUEST_OPTIONS, "model": config["model"],
                                   "messages": [{"role": "system", "content": config["prompt"]},
                                                {"role": "user", "content": text}],
                                   "max_tokens": config["max_tokens"]},
                             timeout=60)
    response.raise_for_status()
    return response.json()


def run(input_path, output, config, max_calls=2, caller=call_model):
    if max_calls < 0:
        raise ValueError("max_calls must be nonnegative")
    rows = read_rows(input_path)
    output.mkdir(parents=True, exist_ok=True)
    results = output / "results.jsonl"
    with run_lock(output):
        run_id = uuid4().hex
        configuration = {**config, "endpoint": API_URL, "schema": "labels-v2",
                         "request_options": REQUEST_OPTIONS}
        input_hash = digest(rows)
        batch_key = digest({"input": input_hash, "config": configuration})
        metadata = {"run_id": run_id, "started_utc": now(), "input_file": input_path.name,
                    "input_hash": input_hash, "batch_key": batch_key,
                    "config": configuration, "max_calls": max_calls}
        # Every invocation gets its own metadata, including a fully skipped run.
        (output / (run_id + ".json")).write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        completed = completed_keys(results)
        counts = {"calls": 0, "skipped": 0, "format_ok": 0, "errors": 0}
        for row in rows:
            request_key = digest({"batch_key": batch_key, "row": row})
            if request_key in completed:
                counts["skipped"] += 1
                continue
            if counts["calls"] >= max_calls:
                break
            record = {"run_id": run_id, "request_key": request_key, **row,
                      "timestamp_utc": now(), "model_requested": config["model"],
                      "status": "error", "raw_model_output": None,
                      "parsed_output": None, "provider_response": None,
                      "model_returned": None, "error": None}
            counts["calls"] += 1
            try:
                data = caller(row["response"], config)
                record["provider_response"] = data
                record["model_returned"] = data.get("model")
                choice = data["choices"][0]
                raw = choice["message"]["content"]
                record["raw_model_output"] = raw
                if choice.get("finish_reason") != "stop":
                    raise ValueError("Output did not finish normally")
                record["parsed_output"] = validate_output(raw)
                record["status"] = "format_ok"
                counts["format_ok"] += 1
            except Exception as exc:
                # Exception messages may contain request URLs or credentials.
                record["error"] = type(exc).__name__
                counts["errors"] += 1
            append_record(results, record)
        append_record(output / "runs.jsonl", {"run_id": run_id, "finished_utc": now(), **counts})
        return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=HERE / "input_responses.csv")
    parser.add_argument("--output", type=Path, default=HERE / "output")
    parser.add_argument("--max-calls", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = {"model": os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
              "prompt": SYSTEM_PROMPT, "max_tokens": 1024}
    if args.dry_run:
        rows = read_rows(args.input)
        print(json.dumps({"rows": len(rows), "config": config,
                          "max_calls": args.max_calls}, ensure_ascii=False, indent=2))
        return
    if not os.getenv("DEEPSEEK_API_KEY"):
        parser.error("Set DEEPSEEK_API_KEY in this session first, or use --dry-run.")
    print(json.dumps(run(args.input, args.output, config, args.max_calls)))


if __name__ == "__main__":
    main()
