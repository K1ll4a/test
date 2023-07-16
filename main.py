import pyowm, datetime

api_key = '36be05764b5968a7d76c7d9e24e2daab'  # your API Key here as string
owm = pyowm.OWM(api_key).weather_manager()  # Use API key to get data
city = input("Enter the name of the city: ")


def print_weather(data):
    ref_time = datetime.datetime.fromtimestamp(data.ref_time).strftime('%Y-%m-%d %H:%M')
    print(f"Time\t\t: {ref_time}")
    print(f"Temperature\t: {data.temperature('celsius')['temp']}")
    if data.rain:
        print(f"Rain: true")
    print("\n")


def get_current_weather():
    weather_api = owm.weather_at_place(city)  # give where you need to see the weather
    weather_data = weather_api.weather  # get out data in the mentioned location

    print("***Current Weather***")
    print_weather(weather_data)
    print("\n")


def get_forecast_weather():
    print("***5 day forecast Weather***")
    forecast_at_place = []
    for item in owm.forecast_at_place(city, '3h').forecast:
        forecast_at_place.append(item)

    forcast_at_place_days = cast_to_days(forecast_at_place)

    for item in forcast_at_place_days:
        print_weather(item)


def cast_to_days(data):
    new_data = []

    for i in range(len(data) - 1):
        day = data[i]
        week_day = datetime.datetime.fromtimestamp(data[i].ref_time).weekday()

        if len(new_data) != 0:
            if week_day == datetime.datetime.fromtimestamp(new_data[-1].ref_time).weekday():
                continue

        times = 0
        for j in range(i + 1, len(data) - 1):
            next_item_week_day = datetime.datetime.fromtimestamp(data[j].ref_time).weekday()
            if week_day == next_item_week_day:
                times += 1
                if data[j].rain:
                    day.rain = data[j].rain
                day.temperature('celsius')['temp'] += data[j].temperature('celsius')['temp']

        day.temperature('celsius')['temp'] /= times
        new_data.append(day)

    return new_data


if __name__ == '__main__':
    get_current_weather()
    get_forecast_weather()
