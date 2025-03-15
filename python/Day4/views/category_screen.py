import tkinter as tk

class CategoryScreen:
    def __init__(self, root, controller):
        self.frame = tk.Frame(root, bg="#fff3e0")
        self.controller = controller
        tk.Label(self.frame, text="Categories", font=("Helvetica", 36, "bold"), bg="#fff3e0", fg="#f39c12").pack(pady=50)
        for category in self.controller.get_categories():
            tk.Button(self.frame, text=category["name"], font=("Helvetica", 18), command=lambda cid=category["id"]: self.controller.show_recipes(cid)).pack()
