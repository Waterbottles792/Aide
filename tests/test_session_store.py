import tempfile
import unittest
from pathlib import Path

from aide.app.backend.session_store import SessionStore


class SessionStoreTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.store = SessionStore(storage_dir=Path(self.tempdir.name))

    def tearDown(self):
        self.tempdir.cleanup()

    def test_create_and_get_session(self):
        created = self.store.create_session(name="Test Session", summary="Notes", hint_level="beginner")
        self.assertIn("session_id", created)
        self.assertEqual(created["name"], "Test Session")
        self.assertEqual(created["summary"], "Notes")

        loaded = self.store.get_session(created["session_id"])
        self.assertEqual(loaded["session_id"], created["session_id"])
        self.assertEqual(loaded["summary"], "Notes")

    def test_list_sessions_includes_turn_count(self):
        created = self.store.create_session(history=[{"role": "user", "content": "hello"}])
        sessions = self.store.list_sessions()
        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0]["session_id"], created["session_id"])
        self.assertEqual(sessions[0]["turns"], 1)

    def test_save_session_updates_history_and_summary(self):
        created = self.store.create_session(name="Test", summary="Old", history=[{"role": "user", "content": "first"}])
        created["summary"] = "Updated"
        created["history"] = [
            {"role": "user", "content": "first"},
            {"role": "assistant", "content": "next"},
        ]
        saved = self.store.save_session(created)
        self.assertEqual(saved["summary"], "Updated")
        self.assertEqual(len(saved["history"]), 2)

        loaded = self.store.get_session(created["session_id"])
        self.assertEqual(loaded["summary"], "Updated")
        self.assertEqual(len(loaded["history"]), 2)

    def test_delete_session(self):
        created = self.store.create_session(name="DeleteMe")
        self.assertTrue(self.store.delete_session(created["session_id"]))
        self.assertIsNone(self.store.get_session(created["session_id"]))


if __name__ == "__main__":
    unittest.main()
