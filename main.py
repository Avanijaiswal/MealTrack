import os
import sys
from dotenv import load_dotenv
from camera.camera import capture_from_camera
from logmeal.logmeal_api import recognize_food, get_nutrition
from database.database import log_meal_json

load_dotenv() 

FLAG_THRESHOLDS = {
    "high_calories": 700, "high_sodium": 800, "high_sugars": 25,
    "low_protein": 10, "high_protein": 25, "high_fiber": 6, "low_fiber": 2
}

def check_health_flags(nutrients_dict, calories):
    flags = []
    def get_qty(key): return nutrients_dict.get(key, {}).get("quantity", 0)

    sodium, sugars, protein, fiber = get_qty("NA"), get_qty("SUGAR"), get_qty("PROCNT"), get_qty("FIBTG")

    if calories is not None and calories >= FLAG_THRESHOLDS["high_calories"]:
        flags.append(f"High calorie meal ({calories:.0f} kcal)")
    if sodium >= FLAG_THRESHOLDS["high_sodium"]:
        flags.append(f"High sodium ({sodium:.0f} mg)")
    if sugars >= FLAG_THRESHOLDS["high_sugars"]:
        flags.append(f"High sugar content ({sugars:.0f} g)")
    if protein >= FLAG_THRESHOLDS["high_protein"]:
        flags.append(f"Good protein source ({protein:.0f} g)")
    elif protein <= FLAG_THRESHOLDS["low_protein"]:
        flags.append(f"Low protein contribution ({protein:.0f} g)")
    if fiber >= FLAG_THRESHOLDS["high_fiber"]:
        flags.append(f"Good source of fiber ({fiber:.0f} g)")
    elif fiber <= FLAG_THRESHOLDS["low_fiber"]:
        flags.append(f"Low fiber ({fiber:.0f} g)")

    return flags if flags else ["No notable flags - looks like a balanced meal."]


def print_report(dish_name, nutrition_data):
    print("\n" + "=" * 40)
    print(f" FOOD REPORT: {dish_name.title()}")
    print("=" * 40)
 
    info = nutrition_data.get("nutritional_info", {})
    if not info:
        print("No detailed nutrition data was found for this item.")
        return
 
    calories = info.get("calories")
    if calories is not None:
        print(f"Calories: {calories} kcal\n")
 
    nutrients = info.get("totalNutrients", {})
    for key, details in nutrients.items():
        label = details.get("label", key)
        quantity = details.get("quantity", 0)
        unit = details.get("unit", "")
        print(f"  {label:<25}: {quantity:.2f} {unit}")

    flags = check_health_flags(nutrients, calories)
    print("\nHealth flags:")
    for flag in flags:
        print(f"  {flag}")

    log_meal_json(dish_name, nutrients, calories, flags)
    print("=" * 40 + "\n")
 

def main():
    if len(sys.argv) >= 2:
        image_path = sys.argv[1]
        if not os.path.exists(image_path):
            print(f"ERROR: Could not find file '{image_path}'")
            sys.exit(1)
    else:
        image_path = capture_from_camera()
        if image_path is None:
            print("No photo captured. Exiting.")
            sys.exit(0)

    print(f"Analyzing {image_path} ...")
 
    recognition = recognize_food(image_path)
    print(f"Detected dish: {recognition['dish_name']}")
 
    nutrition_data = get_nutrition(recognition["image_id"])
    print_report(recognition["dish_name"], nutrition_data)
 
if __name__ == "__main__":
    main()