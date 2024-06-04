import requests
from pprint import pprint as pp

# place API key here - attempted to place in separate file but was unsuccessful
API_KEY = 'c7a1471cd663eef102837d1c390b379c'


def get_weather_data(city):
    endpoint = 'https://api.openweathermap.org/data/2.5/weather'
    payload = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    response = requests.get(endpoint, params=payload)

    # use this status code to see if there are any errors (if API isn't working).
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Sorry, we are unable to retrieve this info right now: {response.status_code}")
        return None


def format_weather_data(data):
    # change data into readable format

    temperature = data['main']['temp']
    weather_description = data['weather'][0]['description']

    # Using string slicing to get a shorter description
    short_description = weather_description[:9]

    # Uppercase function
    weather_upper = weather_description.upper()

    return {
        "temperature": temperature,
        "weather_description": weather_description,
        "short_description": short_description,
        "weather_upper": weather_upper
    }


def recommend_activity(weather):

    # What activities are suitable for this weather?
    # return recs based on the weather forecast

    if 'rain' in weather.lower():
        return "The weather isn't on your side, so it's time to find a coffee shop, or perhaps enjoy a museum day?."
    elif 'clear' in weather.lower() or 'sunny' in weather.lower():
        return "Bring your beach towels and SPF!"
    elif 'cloud' in weather.lower():
        return "It's perfect weather for a hike, or maybe join a walking tour?."
    elif 'snow' in weather.lower():
        return "...Do you wanna build a snowman?"
    else:
        return "Enjoy the sights, ask around for the local activities and maybe get ready for some fun night life."


def write_to_file(filename, data):

    # add results to separate file called results
    # params : filename (write results to), data (make into list)

    with open(filename, 'w') as file:
        for entry in data:
            city, weather_data = next(iter(entry.items()))
            file.write(f"City: {city}\n")
            if isinstance(weather_data, dict):
                file.write(f"Temperature: {weather_data['temperature']}°C\n")
                file.write(f"Weather Description: {weather_data['weather_description']}\n")
                file.write(f"Short Description: {weather_data['short_description']}\n")
                file.write(f"Recommendation: {weather_data['recommendation']}\n")
            else:
                file.write(f"Error: {weather_data}\n")
            file.write("\n")


def main():
    # main function for app to work
    # Prompt the user to enter city names separated by commas
    cities = input("Which city's weather forecast would you like to know? (use commas for multiple): ").split(',')
    cities = [city.strip() for city in cities]

    results = []
    for city in cities:
        weather_data = get_weather_data(city)
        if weather_data:
            transformed_data = format_weather_data(weather_data)
            recommendation = recommend_activity(transformed_data['weather_description'])
            transformed_data['recommendation'] = recommendation
            results.append({city: transformed_data})
        else:
            results.append({city: "Failed to get weather data"})

    write_to_file('results.txt', results)

    # Print the results to the console using pprint
    for result in results:
        pp(result)


if __name__ == "__main__":
    main()
