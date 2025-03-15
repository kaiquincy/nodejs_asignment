from pymongo import MongoClient
from PIL import Image, ImageTk
import random
import os

client = MongoClient('mongodb://localhost:27017/')
db = client['recipe_manager']
feedback_collection = db['feedback']

categories = [
    {"id": 1, "name": "Main Courses"},
    {"id": 2, "name": "Desserts"},
    {"id": 3, "name": "Appetizers"},
    {"id": 4, "name": "Beverages"},
]

recipes = [
    {"id": 1, "categoryId": 1, "name": "Spiced Bean Tacos", "ingredients": "Lettuce, beans", "steps": "Mix & Serve", "time": "25 min", "serves": "2"},
    {"id": 2, "categoryId": 2, "name": "Chocolate Cake", "ingredients": "Flour, cocoa", "steps": "Bake", "time": "50 min", "serves": "8"},
]

def save_feedback(recipe_name, feedback_text):
    feedback_collection.insert_one({"recipeId": recipe_name, "feedback": feedback_text})

def get_feedbacks(recipe_name):
    return list(feedback_collection.find({"recipeId": recipe_name}))

def get_random_image():
    image_files = [f"food{i}.jpeg" for i in range(1, 3)]
    image_path = os.path.join("images", random.choice(image_files))
    try:
        img = Image.open(image_path).resize((400, 300), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except FileNotFoundError:
        return None