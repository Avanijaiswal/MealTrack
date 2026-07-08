import os
import sys
from dotenv import load_dotenv
from camera.camera import capture_from_camera
from logmeal.logmeal_api import recognize_food, get_nutrition
from database.database import log_meal_json

load_dotenv()   #reads Key-valye pairs from .env

def check_health_flags(nutrients, calories):  #nutrients are the data fetched from the api and has been parsed in py dict
    flags = []
    
    def get_value(nutrient_key):     #helper func which extracts the data from the api
        return nutrients.get(nutrient_key, {}).get("quantity", 0)

    sodium = get_value("NA")
    sugars = get_value("SUGAR")
    protein = get_value("PROCNT")
    fiber = get_value("FIBTG")

    if calories is not None and calories >= 700:
        flags.append(f"High calorie: {int(calories)} kcal")
    
    if sodium >= 800:
        flags.append(f"High sodium: {int(sodium)} mg")
        
    if sugars >= 25:
        flags.append(f"High sugar: {int(sugars)} g")
        
    if protein >= 25:
        flags.append(f"Good protein: {int(protein)} g")
    elif protein <= 10:
        flags.append(f"Low protein: {int(protein)} g")
        
    if fiber >= 6:
        flags.append(f"Good fiber: {int(fiber)} g")
    elif fiber <= 2:
        flags.append(f"Low fiber: {int(fiber)} g")

    if len(flags) == 0:
        return ["Balanced meal!"]
    return flags

def print_report(dish_name, nutrition_data):    #nutrition_data, data fetched from the api and has been parsed in py dict
    print(f"\n--- FOOD REPORT: {dish_name.upper()} ---")
 
    info = nutrition_data.get("nutritional_info", {})
    if not info:
        print("No nutritional data found.")
        return
 
    calories = info.get("calories")
    if calories:
        print(f"Calories: {calories} kcal")
 
    print("Nutrients:")
    nutrients = info.get("totalNutrients", {})
    for key, details in nutrients.items():
        name = details.get("label")
        amount = details.get("quantity")
        unit = details.get("unit")
        print(f" - {name}: {amount:.2f} {unit}")

    flags = check_health_flags(nutrients, calories)
    print("\nHealth Notes:")
    for flag in flags:
        print(f" * {flag}")

    log_meal_json(dish_name, nutrients, calories, flags)       #save to database


def main():
    if len(sys.argv) >= 2:
        image_path = sys.argv[1]
    else:
        image_path = capture_from_camera()
        
    if not image_path:
        print("No image provided. Exiting.")
        return

    print(f"Analyzing {image_path}...")
    recognition = recognize_food(image_path)
    dish_name = recognition['dish_name']
    image_id = recognition['image_id']
    
    print(f"Detected: {dish_name}")
 
    nutrition_data = get_nutrition(image_id)
    print_report(dish_name, nutrition_data)   
   
if __name__ == "__main__":
    main()
    



 

# def main():
    
#     if len(sys.argv) >= 2:
#         image_path = sys.argv[1]
#         if not os.path.exists(image_path):
#             print(f"ERROR: Could not find file '{image_path}'")
#             sys.exit(1)
#     else:
#         image_path = capture_from_camera()
#         if image_path is None:
#             print("No photo captured. Exiting.")
#             sys.exit(0)

#     print(f"Analyzing {image_path} ...")
 
#     recognition = recognize_food(image_path)     #logmeal
#     print(f"Detected dish: {recognition['dish_name']}")
 
#     nutrition_data = get_nutrition(recognition["image_id"])  #logmeal
    
#     print_report(recognition["dish_name"], nutrition_data)   
   
# if __name__ == "__main__":
#     main()