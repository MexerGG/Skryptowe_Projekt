import json
import os

class VotingLogic:
    def __init__(self, user_file="signup.json", vote_file="votecount.json"):
        self.user_file = user_file
        self.vote_file = vote_file
        self.uzytkownicy = []
        self.votes = [0, 0, 0, 0, 0]
        self.load_users()
        self.load_votes()

    def load_users(self):
        if os.path.exists(self.user_file):
            with open(self.user_file, "r") as f:
                try:
                    self.uzytkownicy = json.load(f)
                except json.JSONDecodeError:
                    self.uzytkownicy = []

    def save_users(self):
        with open(self.user_file, "w") as f:
            json.dump(self.uzytkownicy, f, indent=4)

    def load_votes(self):
        if os.path.exists(self.vote_file):
            with open(self.vote_file, "r") as f:
                try:
                    self.votes = json.load(f)
                except json.JSONDecodeError:
                    self.votes = [0, 0, 0, 0, 0]

    def save_votes(self):
        with open(self.vote_file, "w") as f:
            json.dump(self.votes, f, indent=4)

    # ...reszta bez zmian

    def register_user(self, login, password):
        if not login or not password:
            return False, "Login i hasło nie mogą być puste."
        for user in self.uzytkownicy:
            if user["login"] == login:
                return False, "Login już istnieje."
        self.uzytkownicy.append({"login": login, "password": password, "voted": False})
        self.save_users()
        return True, "Rejestracja zakończona sukcesem."

    def check_login(self, login, password):
        for user in self.uzytkownicy:
            if user["login"] == login and user["password"] == password:
                return True, user["voted"]
        return False, False

    def cast_vote(self, user_login, symbol):
        symbol_map = {'@': 0, '#': 1, '$': 2, '&': 3, 'NOTA': 4}
        for user in self.uzytkownicy:
            if user["login"] == user_login:
                if user["voted"]:
                    return False, "Użytkownik już oddał głos."
                if symbol not in symbol_map:
                    return False, "Niepoprawny symbol głosu."
                self.votes[symbol_map[symbol]] += 1
                user["voted"] = True
                self.save_votes()
                self.save_users()
                return True, "Twój głos został zapisany."
        return False, "Użytkownik nie znaleziony."

    def get_results(self):
        return self.votes.copy()
