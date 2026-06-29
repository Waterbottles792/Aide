import unittest

from aide.app.backend.llm_client import build_mentor_prompt


class BuildMentorPromptTests(unittest.TestCase):
    def test_includes_hint_level_and_challenge_context(self):
        prompt = build_mentor_prompt(
            "I am stuck on a SQL injection challenge",
            hint_level="beginner",
            challenge_context="PortSwigger lab",
            mode="web",
        )

        self.assertIn("You are Aide", prompt)
        self.assertIn("beginner", prompt.lower())
        self.assertIn("PortSwigger lab", prompt)
        self.assertIn("SQL injection", prompt)

    def test_defaults_to_guided_mode(self):
        prompt = build_mentor_prompt("Help me")

        self.assertIn("guided", prompt.lower())
        self.assertIn("teach progressively", prompt.lower())

    def test_includes_recent_session_history(self):
        prompt = build_mentor_prompt(
            "What should I try next?",
            session_history=[
                {"role": "user", "content": "I tried a basic payload"},
                {"role": "assistant", "content": "Try checking the response body"},
            ],
        )

        self.assertIn("session history", prompt.lower())
        self.assertIn("response body", prompt)

    def test_includes_session_summary(self):
        prompt = build_mentor_prompt(
            "What should I try next?",
            session_summary="Working on a TryHackMe web challenge with SQL injection",
        )

        self.assertIn("session summary", prompt.lower())
        self.assertIn("TryHackMe web challenge", prompt)


if __name__ == "__main__":
    unittest.main()
