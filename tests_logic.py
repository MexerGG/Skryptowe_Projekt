import unittest
import os
import json
from logic import VotingLogic

class TestVotingLogic(unittest.TestCase):
    def setUp(self):
        # Użyj alternatywnych plików do testów
        self.signup_path = "signup_test.json"
        self.votecount_path = "votecount_test.json"
        self.logic = VotingLogic(user_file=self.signup_path, vote_file=self.votecount_path)
        self.logic.uzytkownicy = []
        self.logic.votes = [0, 0, 0, 0, 0]
        self.logic.save_users()
        self.logic.save_votes()

    def test_register_user(self):
        success, msg = self.logic.register_user("testuser", "pass123")
        self.assertTrue(success)
        self.assertIn("Rejestracja", msg)
        self.assertEqual(len(self.logic.uzytkownicy), 1)
        self.assertEqual(self.logic.uzytkownicy[0]["login"], "testuser")

        # Rejestracja tego samego loginu
        success2, msg2 = self.logic.register_user("testuser", "pass456")
        self.assertFalse(success2)
        self.assertIn("istnieje", msg2)

    def test_check_login(self):
        self.logic.register_user("testuser", "pass123")
        success, voted = self.logic.check_login("testuser", "pass123")
        self.assertTrue(success)
        self.assertFalse(voted)

        self.assertFalse(self.logic.check_login("wronguser", "pass123")[0])
        self.assertFalse(self.logic.check_login("testuser", "badpass")[0])

    def test_cast_vote_and_prevent_double_vote(self):
        self.logic.register_user("voter", "secret")
        success, msg = self.logic.cast_vote("voter", "@")
        self.assertTrue(success)
        self.assertIn("zapisany", msg)

        # Drugi głos – powinien być zablokowany
        success2, msg2 = self.logic.cast_vote("voter", "#")
        self.assertFalse(success2)
        self.assertIn("odd", msg2.lower())  # sprawdź, że jest info o oddanym głosie

        counts = self.logic.get_results()
        self.assertEqual(counts[0], 1)
        self.assertEqual(sum(counts), 1)

    def test_vote_counts(self):
        self.logic.register_user("u1", "p")
        self.logic.register_user("u2", "p")
        self.logic.cast_vote("u1", "#")
        self.logic.cast_vote("u2", "NOTA")

        counts = self.logic.get_results()
        self.assertEqual(counts[1], 1)  # #
        self.assertEqual(counts[4], 1)  # NOTA
        self.assertEqual(sum(counts), 2)

    def tearDown(self):
        # Usuń pliki testowe
        if os.path.exists(self.signup_path):
            os.remove(self.signup_path)
        if os.path.exists(self.votecount_path):
            os.remove(self.votecount_path)

if __name__ == "__main__":
    unittest.main()
