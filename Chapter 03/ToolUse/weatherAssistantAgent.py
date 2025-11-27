

# This code implements a simple weather agent that fetches weather data from the OpenWeatherMap API.


# Import necessary libraries
import requests

# Weather Agent using OpenWeatherMap API (replace with your API key)
class WeatherAgent:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city="Delhi"):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"The weather in {city} is {weather} with a temperature of {temp}°C."
        else:
            return "Failed to retrieve weather data."


# Example usage
if __name__ == "__main__":
    API_KEY = "your_api_key"  # Replace with your actual API key
    agent = WeatherAgent(API_KEY)
    print(agent.get_weather("Noida"))

#output: The weather in Delhi is haze with a temperature of 32.05°C.




