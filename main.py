import pyowm, datetime

api_key = '36be05764b5968a7d76c7d9e24e2daab'  # your API Key here as string
owm = pyowm.OWM(api_key).weather_manager()  # Use API key to get data
city = input("Enter the name of the city: ")


def print_weather(data):
    ref_time = datetime.datetime.fromtimestamp(data.ref_time).strftime('%Y-%m-%d %H:%M')
    print(f"Time\t\t: {ref_time}")
    print(f"Overview\t: {data.detailed_status}")
    print(f"Wind Speed\t: {data.wind()}")
    print(f"Humidity\t: {data.humidity}")
    print(f"Temperature\t: {data.temperature('fahrenheit')}")
    print(f"Rain\t\t: {data.rain}")
    print("\n")


def get_current_weather():
    weather_api = owm.weather_at_place(city)  # give where you need to see the weather
    weather_data = weather_api.weather  # get out data in the mentioned location

    print("***Current Weather***")
    print_weather(weather_data)
    print("\n")


def get_forecast_weather():
    print("***5 day forecast Weather***")
    for item in owm.forecast_at_place(city, '3h').forecast:
        print_weather(item)


if __name__ == '__main__':
    get_current_weather()
    get_forecast_weather()