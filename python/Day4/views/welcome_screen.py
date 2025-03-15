import tkinter as tk

class WelcomeScreen:
    def __init__(self, root, controller):
        self.frame = tk.Frame(root, bg="#fff3e0")
        self.controller = controller
        tk.Label(self.frame, text="Welcome to Recipes", font=("Helvetica", 36, "bold"), bg="#fff3e0", fg="#f39c12").pack(pady=50)
        tk.Button(self.frame, text="Start Cooking", font=("Helvetica", 16), bg="#f1c40f", fg="white", command=self.controller.show_categories).pack(pady=30)
