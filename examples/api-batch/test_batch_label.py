import json
import tempfile
import unittest
from pathlib import Path
import batch_label as demo


def reply(raw='{"labels":["other"],"reason":"教学示例"}'):
    return {"model": "returned-demo", "choices": [
        {"finish_reason": "stop", "message": {"content": raw}}]}


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "input.csv"
        self.source.write_text("id,response\n1,one\n2,two\n", encoding="utf-8")
        self.out = self.root / "output"
        self.config = {"model": "demo", "prompt": "prompt", "max_tokens": 1024}

    def run_demo(self, caller=lambda text, config: reply(), limit=10, config=None):
        return demo.run(self.source, self.out, config or self.config, limit, caller)

    def test_resume_same_configuration(self):
        self.assertEqual(self.run_demo()["calls"], 2)
        self.assertEqual(self.run_demo()["calls"], 0)
        self.assertEqual(len(list(self.out.glob("*.json"))), 2)

    def test_changed_input_reruns(self):
        self.run_demo()
        self.source.write_text("id,response\n1,changed\n2,two\n", encoding="utf-8")
        self.assertEqual(self.run_demo()["calls"], 2)

    def test_model_and_prompt_changes_rerun(self):
        self.run_demo()
        self.assertEqual(self.run_demo(config={**self.config, "model": "other"})["calls"], 2)
        self.assertEqual(self.run_demo(config={**self.config, "prompt": "new"})["calls"], 2)

    def test_invalid_outputs_remain_retryable(self):
        for raw in ["not json", "[]", '{"labels":["bogus"],"reason":"x"}',
                    '{"labels":["other","rumination"],"reason":"x"}',
                    '{"labels":[],"reason":"x"}', '{"labels":["other"],"reason":""}']:
            with self.subTest(raw=raw):
                self.assertEqual(self.run_demo(lambda text, config: reply(raw))["errors"], 2)
        self.assertEqual(self.run_demo()["format_ok"], 2)
        records = [json.loads(x) for x in (self.out / "results.jsonl").read_text(
            encoding="utf-8").splitlines()]
        self.assertEqual(records[0]["raw_model_output"], "not json")

    def test_partial_failure_resume_and_redaction(self):
        def call(text, config):
            if text == "two":
                raise RuntimeError("SECRET_SHOULD_NOT_BE_LOGGED")
            return reply()
        self.assertEqual(self.run_demo(call)["errors"], 1)
        resumed = self.run_demo()
        self.assertEqual((resumed["calls"], resumed["skipped"]), (1, 1))
        self.assertNotIn("SECRET_SHOULD_NOT_BE_LOGGED",
                         (self.out / "results.jsonl").read_text(encoding="utf-8"))

    def test_cap_and_zero_calls(self):
        self.assertEqual(self.run_demo(limit=0)["calls"], 0)
        self.assertEqual(self.run_demo(limit=1)["calls"], 1)
        self.assertEqual(self.run_demo(limit=1)["calls"], 1)

    def test_duplicate_id_rejected_before_call(self):
        self.source.write_text("id,response\n1,a\n1,b\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.run_demo()

    def test_truncated_response_not_success(self):
        def call(text, config):
            result = reply()
            result["choices"][0]["finish_reason"] = "length"
            return result
        self.assertEqual(self.run_demo(call)["errors"], 2)

    def test_torn_last_line_preserved_and_recoverable(self):
        self.run_demo(limit=1)
        with (self.out / "results.jsonl").open("a", encoding="utf-8") as stream:
            stream.write('{"interrupted":')
        self.assertEqual(self.run_demo()["calls"], 1)
        self.assertEqual(self.run_demo()["calls"], 0)

    def test_parallel_run_guard(self):
        self.out.mkdir()
        (self.out / ".running").write_text("test", encoding="utf-8")
        with self.assertRaises(RuntimeError):
            self.run_demo()


if __name__ == "__main__":
    unittest.main()
