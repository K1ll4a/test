import pyowm, datetime

api_key = '36be05764b5968a7d76c7d9e24e2daab'  # your API Key here as string
owm = pyowm.OWM(api_key).weather_manager()  # Use API key to get data
city = input("Enter the name of the city: ")


def get_weather():
    print("***5 day forecast Weather***")
    data = get_data()

    for item in data:
        print_weather(item)


def get_day_weather():
    print("***Certain day forecast Weather***")
    data = get_data()

    for item in data:
        print_weather(item)


def get_current_weather():
    print("***Current day forecast Weather***")
    data = get_data()

    for item in data:
        print_weather(item)


def get_data():
    weather_at_place_3h = []
    for item in owm.forecast_at_place(city, "3h").forecast:
        weather_at_place_3h.append(item)

    return cast_to_days(weather_at_place_3h)


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


def print_weather(data):
    ref_time = datetime.datetime.fromtimestamp(data.ref_time).strftime('%Y-%m-%d %H:%M')
    print(f"Time\t\t: {ref_time}")
    print(f"Temperature\t: {data.temperature('celsius')['temp']}")
    if data.rain:
        print(f"Rain: true")
    print("\n")


if __name__ == '__main__':
    get_weather()
    get_day_weather()
    get_current_weather()


