import json
import tempfile
import unittest
from pathlib import Path

from aide.cli import load_config, save_config


class CliConfigTests(unittest.TestCase):
    def test_save_and_load_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.json"
            payload = {
                "provider": "groq",
                "api_key": "abc123",
                "model": "llama-3.1-8b-instant",
                "platform": "tryhackme",
                "room": "basic-recon",
            }
            save_config(payload, path=path)
            loaded = load_config(path=path)
            self.assertEqual(loaded["provider"], "groq")
            self.assertEqual(loaded["api_key"], "abc123")
            self.assertEqual(loaded["room"], "basic-recon")

            raw = json.loads(path.read_text())
            self.assertEqual(raw["provider"], "groq")


if __name__ == "__main__":
    unittest.main()
