import random

def weather_system():
    weather = {
            1:"hot",
            2:"cold",
            3:"rainy",
            4:"thunder_storm"}

    
    keys = list(weather.keys())

    random_key = random.choice(keys)

    random_weather_value = weather[random_key]

    return random_weather_value

    



print(weather_system())