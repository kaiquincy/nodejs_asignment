import tkinter as tk

class RecipeDetailScreen:
    def __init__(self, root, controller):
        self.frame = tk.Frame(root, bg="#fff3e0")
        self.controller = controller
        tk.Label(self.frame, text="Recipe Details", font=("Helvetica", 36, "bold"), bg="#fff3e0", fg="#f39c12").pack(pady=50)
        self.image_label = tk.Label(self.frame, bg="#fff3e0", borderwidth=2, relief="solid")
        self.image_label.pack(pady=10)
    
    def update_details(self, recipe):
        tk.Label(self.frame, text=recipe["name"], font=("Helvetica", 24, "bold")).pack()
        tk.Label(self.frame, text=f"Time: {recipe['time']}, Serves: {recipe['serves']}").pack()
        
        image = self.controller.get_random_image()
        print(image)
        if image:
            print("have img_")
            self.image_label.image = image
            self.image_label.config(image=image)