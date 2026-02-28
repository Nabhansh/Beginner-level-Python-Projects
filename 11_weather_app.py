# ============================================================
# PROJECT 11: Weather App (API)
# Uses OpenWeatherMap free API
# Get a free API key at: https://openweathermap.org/api
# ============================================================

import urllib.request
import json
import sys

# 🔑 Replace with your API key from openweathermap.org (free tier)
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

WEATHER_ICONS = {
    "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️",
    "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Snow": "❄️",
    "Mist": "🌫️", "Fog": "🌫️", "Haze": "🌫️",
    "Dust": "💨", "Sand": "💨", "Smoke": "💨",
    "Tornado": "🌪️"
}

def fetch_json(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        print(f"  ❌ Network error: {e.reason}")
        return None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def get_weather(city, units="metric"):
    if API_KEY == "YOUR_API_KEY_HERE":
        print("\n  ⚠️  Demo Mode: No API key set.")
        print("  Get a free key at: https://openweathermap.org/api")
        print("  Then replace 'YOUR_API_KEY_HERE' in the script.\n")
        show_demo_weather(city)
        return

    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units={units}"
    data = fetch_json(url)

    if not data:
        return

    if data.get("cod") != 200:
        print(f"  ❌ Error: {data.get('message', 'Unknown error')}")
        return

    temp_unit = "°C" if units == "metric" else "°F"
    speed_unit = "m/s" if units == "metric" else "mph"

    weather_main = data["weather"][0]["main"]
    icon = WEATHER_ICONS.get(weather_main, "🌡️")

    print(f"\n{'='*50}")
    print(f"  {icon} Weather in {data['name']}, {data['sys']['country']}")
    print(f"{'='*50}")
    print(f"  Condition:   {data['weather'][0]['description'].title()}")
    print(f"  Temperature: {data['main']['temp']:.1f}{temp_unit}")
    print(f"  Feels Like:  {data['main']['feels_like']:.1f}{temp_unit}")
    print(f"  Min/Max:     {data['main']['temp_min']:.1f}{temp_unit} / {data['main']['temp_max']:.1f}{temp_unit}")
    print(f"  Humidity:    {data['main']['humidity']}%")
    print(f"  Pressure:    {data['main']['pressure']} hPa")
    print(f"  Wind:        {data['wind']['speed']} {speed_unit}, {data['wind'].get('deg', 0)}°")
    print(f"  Visibility:  {data.get('visibility', 'N/A')} m")
    print(f"  Clouds:      {data['clouds']['all']}%")
    print(f"{'='*50}")

def show_demo_weather(city):
    """Demo output when no API key is set"""
    import random
    conditions = ["Partly Cloudy", "Sunny", "Light Rain", "Overcast"]
    temps = random.randint(15, 35)
    cond = random.choice(conditions)
    print(f"\n{'='*50}")
    print(f"  ☀️ DEMO Weather in {city.title()}")
    print(f"{'='*50}")
    print(f"  Condition:   {cond}  (DEMO DATA)")
    print(f"  Temperature: {temps}°C")
    print(f"  Feels Like:  {temps - random.randint(0,3)}°C")
    print(f"  Humidity:    {random.randint(40, 80)}%")
    print(f"  Wind:        {random.randint(5, 25)} m/s")
    print(f"  Note: Add your API key for real weather data!")
    print(f"{'='*50}")

def main():
    print("=" * 50)
    print("        🌤️  WEATHER APP")
    print("=" * 50)
    print("Data powered by OpenWeatherMap API")
    print("Type 'quit' to exit\n")

    units = "metric"
    print("Units: 1) Metric (°C)  2) Imperial (°F)")
    if input("Choose (1/2, default=1): ").strip() == '2':
        units = "imperial"

    while True:
        city = input("\nEnter city name: ").strip()
        if city.lower() == 'quit':
            print("\n👋 Goodbye!")
            break
        if not city:
            continue
        get_weather(city, units)

if __name__ == "__main__":
    main()
