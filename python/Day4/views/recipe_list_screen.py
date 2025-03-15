import tkinter as tk

class RecipeListScreen:
    def __init__(self, root, controller):
        self.frame = tk.Frame(root, bg="#fff3e0")
        self.controller = controller
        tk.Label(self.frame, text="Recipes", font=("Helvetica", 36, "bold"), bg="#fff3e0", fg="#f39c12").pack(pady=50)
    
    def update_recipes(self, recipes):
        for recipe in recipes:
            tk.Button(self.frame, text=recipe["name"], font=("Helvetica", 18), command=lambda rid=recipe["id"]: self.controller.show_recipe_detail(rid)).pack()