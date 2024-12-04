from fastapi import FastAPI, HTTPException
import requests
import os

# Load the config file
with open("config.json", "r") as config_file:
    config = json.load(config_file)
API_KEY = config["API_KEY"]

app = FastAPI()

def format_weather_data(data):
    # Grabbing only relevant info and making it more readable
    return {
        "location": data.get("name"),
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"].capitalize(),
        "wind_speed": data["wind"]["speed"]
    }

# Weather endpoint
@app.get("/weather")
def get_weather():
    mason_url = f"https://api.openweathermap.org/data/2.5/weather?q=Mason,US&appid={API_KEY}&units=imperial"
    crystal_lake_url = f"https://api.openweathermap.org/data/2.5/weather?q=Crystal%20Lake,US&appid={API_KEY}&units=imperial"

    mason_response = requests.get(mason_url)
    crystal_response = requests.get(crystal_lake_url)

    # Error checking
    if mason_response.status_code != 200:
        raise HTTPException(status_code=mason_response.status_code, detail=f"Error fetching Mason weather: {mason_response.json()}")
    if crystal_response.status_code != 200:
        raise HTTPException(status_code=crystal_response.status_code, detail=f"Error fetching Crystal Lake weather: {crystal_response.json()}")

    mason_weather = format_weather_data(mason_response.json())
    crystal_weather = format_weather_data(crystal_response.json())

    return {
        "Mason": mason_weather,
        "Crystal Lake": crystal_weather
    }
