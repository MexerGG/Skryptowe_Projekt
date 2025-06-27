from logic import VotingLogic
import time
import unittest
import pytest
from memory_profiler import profile
import flake8.api.legacy as flake8

# Testy jednostkowe
class TestVotingLogic(unittest.TestCase):
    def setUp(self):
        self.logic = VotingLogic(user_file="test_users.json", vote_file="test_votes.json")
        self.logic.uzytkownicy = []
        self.logic.votes = [0, 0, 0, 0, 0]

    def test_register_user(self):
        success, msg = self.logic.register_user("test", "pass")
        self.assertTrue(success)

    def test_duplicate_user(self):
        self.logic.register_user("test", "pass")
        success, _ = self.logic.register_user("test", "pass")
        self.assertFalse(success)

    def test_vote_sum_recursive(self):
        self.logic.votes = [1, 2, 3]
        self.assertEqual(self.logic.recursive_vote_sum(), 6)

# Testy funkcjonalne (pytest)
def test_login():
    logic = VotingLogic(user_file="test_users.json", vote_file="test_votes.json")
    logic.register_user("user", "pass")
    success, voted = logic.check_login("user", "pass")
    assert success
    assert not voted

# Testy graniczne
def test_vote_invalid_symbol():
    logic = VotingLogic()
    logic.register_user("x", "y")
    success, msg = logic.cast_vote("x", "X")
    assert not success

# Testy wydajności
def test_vote_performance():
    logic = VotingLogic()
    start = time.time()
    for _ in range(10000):
        logic.votes[0] += 1
    end = time.time()
    assert end - start < 1.0

# Testy pamięci
@profile
def test_memory():
    logic = VotingLogic()
    for _ in range(100000):
        logic.votes.append(1)

# Test jakości kodu
def run_flake8():
    style_guide = flake8.get_style_guide()
    report = style_guide.check_files(["logic.py"])
    assert report.total_errors == 0

if __name__ == '__main__':
    unittest.main()
