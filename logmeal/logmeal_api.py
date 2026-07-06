import os
import requests

BASE_URL = "https://api.logmeal.com/v2"

def get_headers():
    """Dynamically builds headers using the loaded environment token."""
    token = os.getenv("LOGMEAL_API_TOKEN")
    if not token:
        raise Exception("API token not found. Check your .env file and load_dotenv().")
    return {"AUTHORIZATION": f"Bearer {token}"}


def recognize_food(image_path):
    url = f"{BASE_URL}/image/segmentation/complete"
    
    with open(image_path, "rb") as img_file:
        files = {"image": img_file}
        # Call get_headers() inside the request
        response = requests.post(url, headers=get_headers(), files=files)

    if response.status_code != 200:
        raise Exception(f"Recognition failed: {response.status_code} - {response.text}")
    
    data = response.json()
    segmentation_results = data.get("segmentation_results", [])

    dish_name = "Unknown"
    if segmentation_results:
        recognition_results = segmentation_results[0].get("recognition_results", [])
        if recognition_results:
            dish_name = recognition_results[0].get("name", "Unknown")
 
    return {"image_id": data.get("imageId"), "dish_name": dish_name}


def get_nutrition(image_id):
    url = f"{BASE_URL}/nutrition/recipe/nutritionalInfo"
    # Call get_headers() inside the request
    response = requests.post(url, headers=get_headers(), json={"imageId": image_id})
    
    if response.status_code != 200:
        raise Exception(f"Nutrition lookup failed: {response.status_code} - {response.text}")
    return response.json()