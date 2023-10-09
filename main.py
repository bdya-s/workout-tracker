import os

import requests
from datetime import datetime

APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")

exercise_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_input = input("Enter your exercise info for the day: ")
exercise_headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
    "x-remote-user-id": "0"
}
query = {
    "query": exercise_input,
    "gender": "female",
    "weight_kg": 65,
    "height_cm": 173,
    "age": 39
}

# Use natural language API to translet your exercise entry.
response = requests.post(exercise_url, headers=exercise_headers, json=query)
data = response.json()["exercises"]


dt_info = datetime.today()
date_today = datetime.strftime(dt_info, '%m/%d/%Y')
time_today = datetime.strftime(dt_info, '%X')

header_param = {
    "Authorization": "Bearer thisisasecret",
    "Content-Type": "application/json"
}
for exercise in data:
    query = {
        "workout": {
            "date": date_today,
            "time": time_today,
            "exercise": exercise["user_input"],
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
            }
        }
    # Use Sheety generated endpoint to log daily exercise info into your Google sheets
    rsp = requests.post(url=SHEET_ENDPOINT, headers=header_param, json=query)

# I jumped for 20 mins, cardio for 50 mins, streching for 90 minutes and Physical Therapy for 1.5 hours