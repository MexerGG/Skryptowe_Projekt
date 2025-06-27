    import tkinter as tk
    from tkinter import messagebox, ttk
    import matplotlib.pyplot as plt
    from logic import VotingLogic

    class VotingSystem:
        def __init__(self, root):
            self.root = root
            self.root.title("System Głosowania")
            self.root.geometry("800x600")
            self.logic = VotingLogic()
            self.login = ""
            self.oddano_glos = False
            self.main_screen()

        def main_screen(self):
            for widget in self.root.winfo_children():
                widget.destroy()

            tk.Label(self.root, text="Witaj w Systemie Głosowania!", font=("Helvetica", 22)).pack(pady=30)
            tk.Button(self.root, text="Zarejestruj się", font=("Helvetica", 14), command=self.register_screen, width=25).pack(pady=10)
            tk.Button(self.root, text="Zaloguj się", font=("Helvetica", 14), command=self.login_screen, width=25).pack(pady=10)
            tk.Button(self.root, text="Zamknij", font=("Helvetica", 14), command=self.root.quit, width=25).pack(pady=30)

        def register_screen(self):
            register_win = tk.Toplevel(self.root)
            register_win.title("Rejestracja")
            register_win.geometry("300x200")
            register_win.transient(self.root)
            register_win.grab_set()
            register_win.attributes('-topmost', True)

            tk.Label(register_win, text="Login:").pack(pady=5)
            login_entry = tk.Entry(register_win)
            login_entry.pack(pady=5)

            tk.Label(register_win, text="Hasło:").pack(pady=5)
            password_entry = tk.Entry(register_win, show="*")
            password_entry.pack(pady=5)

            def submit_register():
                u = login_entry.get()
                p = password_entry.get()
                success, message = self.logic.register_user(u, p)
                if success:
                    messagebox.showinfo("Sukces", message)
                    register_win.destroy()
                else:
                    messagebox.showerror("Błąd", message)

            tk.Button(register_win, text="Zarejestruj się", command=submit_register).pack(pady=20)

        def login_screen(self):
            login_win = tk.Toplevel(self.root)
            login_win.title("Logowanie")
            login_win.geometry("300x200")
            login_win.transient(self.root)
            login_win.grab_set()
            login_win.attributes('-topmost', True)

            tk.Label(login_win, text="Login:").pack(pady=5)
            login_entry = tk.Entry(login_win)
            login_entry.pack(pady=5)

            tk.Label(login_win, text="Hasło:").pack(pady=5)
            password_entry = tk.Entry(login_win, show="*")
            password_entry.pack(pady=5)

            def submit_login():
                u = login_entry.get()
                p = password_entry.get()
                success, voted = self.logic.check_login(u, p)
                if success:
                    self.login = u
                    self.oddano_glos = voted
                    messagebox.showinfo("Zalogowano", f"Witaj, {u}!")
                    login_win.destroy()
                    self.voting_screen()
                else:
                    messagebox.showerror("Błąd", "Niepoprawne dane logowania.")

            tk.Button(login_win, text="Zaloguj się", command=submit_login).pack(pady=20)

        def voting_screen(self):
            for widget in self.root.winfo_children():
                widget.destroy()

            tk.Label(self.root, text=f"Witaj, {self.login}", font=("Helvetica", 18)).pack(pady=15)

            if self.oddano_glos:
                tk.Label(self.root, text="Już oddałeś głos!", font=("Helvetica", 14), fg="red").pack(pady=20)
            else:
                tk.Label(self.root, text="Oddaj swój głos wybierając kandydata:", font=("Helvetica", 16)).pack(pady=20)

                self.symbol_var = tk.StringVar()
                wybor_box = ttk.Combobox(self.root, textvariable=self.symbol_var, font=("Helvetica", 14), state="readonly", width=25)
                wybor_box['values'] = [
                    '@ - Jan Kowalski',
                    '# - Anna Nowak',
                    '$ - Piotr Wiśniewski',
                    '& - Maria Wójcik',
                    'NOTA'
                ]
                wybor_box.pack(pady=10)

                tk.Button(self.root, text="Zatwierdź głos", font=("Helvetica", 14), command=self.cast_vote).pack(pady=10)

            tk.Button(self.root, text="Zobacz wyniki", font=("Helvetica", 14), command=self.show_results).pack(pady=15)
            tk.Button(self.root, text="Wyloguj się", font=("Helvetica", 14), command=self.main_screen).pack(pady=10)

        def cast_vote(self):
            wybor = self.symbol_var.get()
            if not wybor:
                messagebox.showwarning("Uwaga", "Musisz wybrać kandydata!")
                return

            symbol = 'NOTA' if 'NOTA' in wybor else wybor.split()[0]

            success, message = self.logic.cast_vote(self.login, symbol)
            if not success:
                messagebox.showerror("Błąd", message)
            else:
                messagebox.showinfo("Dziękujemy", message)
                self.oddano_glos = True
                self.voting_screen()

        def show_results(self):
            counts = self.logic.get_results()
            labels = ['Jan Kowalski (@)', 'Anna Nowak (#)', 'Piotr Wiśniewski ($)', 'Maria Wójcik (&)', 'NOTA']
            colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336']

            plt.figure(figsize=(10, 6))
            plt.bar(labels, counts, color=colors)
            plt.title("Wyniki Głosowania")
            plt.xlabel("Kandydaci")
            plt.ylabel("Liczba Głosów")
            plt.xticks(rotation=15)
            plt.tight_layout()

            # Zapisz wykres jako obraz PNG
            plt.savefig("voting_results.png")

            # Wyświetl wykres
            plt.show()

    if __name__ == "__main__":
        root = tk.Tk()
        app = VotingSystem(root)
        root.mainloop()
