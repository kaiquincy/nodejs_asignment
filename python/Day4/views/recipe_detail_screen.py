import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class RecipeDetailScreen:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        # Frame chính
        self.frame = tk.Frame(root, bg="#f8f9fa")
        self.frame.pack(fill="both", expand=True)
        
        # Tiêu đề
        self.title_label = tk.Label(
            self.frame, text="Recipe Details", font=("Helvetica", 36, "bold"), 
            bg="#f8f9fa", fg="#ff6f00"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Khu vực hiển thị ảnh
        self.image_label = tk.Label(self.frame, bg="#ffffff", borderwidth=2, relief="solid")
        self.image_label.grid(row=1, column=0, columnspan=2, pady=15, ipadx=10, ipady=10)
        
        # Nội dung công thức
        self.name_label = tk.Label(self.frame, text="", font=("Helvetica", 24, "bold"), bg="#f8f9fa")
        self.name_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.details_label = tk.Label(self.frame, text="", font=("Helvetica", 14), bg="#f8f9fa")
        self.details_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Ô nhập phản hồi
        self.feedback_label = tk.Label(self.frame, text="Your Feedback:", font=("Helvetica", 14), bg="#f8f9fa")
        self.feedback_label.grid(row=4, column=0, pady=10, sticky="w", padx=20)
        
        self.feedback_entry = tk.Text(self.frame, width=50, height=4, font=("Helvetica", 12))
        self.feedback_entry.grid(row=4, column=1, pady=10, padx=20)
        
        # Nút gửi phản hồi
        self.submit_feedback_button = ttk.Button(self.frame, text="Submit Feedback", command=self.submit_feedback)
        self.submit_feedback_button.grid(row=5, column=1, pady=10, sticky="e", padx=20)
        
        # Nút quay lại
        self.back_button = ttk.Button(self.frame, text="Back", command=self.go_back, style="TButton")
        self.back_button.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Thiết lập phong cách cho nút
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 14), padding=10, background="#ff6f00")
        
        # Hiệu ứng hover
        self.back_button.bind("<Enter>", lambda e: self.back_button.config(style="Hover.TButton"))
        self.back_button.bind("<Leave>", lambda e: self.back_button.config(style="TButton"))
        
        style.configure("Hover.TButton", font=("Helvetica", 14), padding=10, background="#ff8f40")
    
    def update_details(self, recipe):
        self.name_label.config(text=recipe["name"], fg="#343a40")
        self.details_label.config(text=f"Time: {recipe['time']} | Serves: {recipe['serves']}", fg="#495057")
        
        image = self.controller.get_random_image()
        if image:
            self.image_label.image = image
            self.image_label.config(image=image)
        
        # Hiệu ứng fade-in
        for widget in [self.image_label, self.name_label, self.details_label]:
            widget.after(100, lambda w=widget: w.config(fg="#000000"))
    
    def submit_feedback(self):
        feedback = self.feedback_entry.get("1.0", tk.END).strip()
        if feedback:
            print("Feedback submitted:", feedback)
            self.feedback_entry.delete("1.0", tk.END)
    
    def go_back(self):
        self.frame.pack_forget()
        self.controller.show_categories()