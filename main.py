import pyowm, datetime
import argparse
from argparse import ArgumentParser, Namespace


api_key = '36be05764b5968a7d76c7d9e24e2daab'  # your API Key here as string
owm = pyowm.OWM(api_key).weather_manager()  # Use API key to get data
city = "Moscow"  # Enter name of the city
#day_value = input("Enter day: ")  # Enter date


parser = ArgumentParser(
    prog='weather_cli',
    description='The program outputs weather data in a certain city',
    epilog="Abbreviations for dates('mo'-monday,'tu'-tuesday,'we'-wednesday,"
           "'th' - thursday,'fr' - friday, 'sa' - saturday,'sun' - sunday)"
)

subparsers = parser.add_subparsers()
day_parser = subparsers.add_parser("day ", help="Enter the day of the week")
day_parser.add_argument("-v")
args = parser.parse_args()


def get_weather():  # Func for displaying the weather for the week
    print("***5 day forecast Weather***")
    data = get_data()  # Calling a function with framed weather data

    for item in data:  # Data search
        print_weather(item)


def get_day_weather(day, comm):  # Func for getting weather data on a specific day
    print(comm)

    day_num = day_to_num(day)

    data = get_data()  # Calling a function with framed weather data
    for item in data:  # Data search
        if datetime.datetime.fromtimestamp(item.ref_time).weekday() == day_num:   # Checks day_value is equal to one of the five days
            print_weather(item)
            break


def get_data():  # Function  for displaying weather data
    weather_at_place_3h = []
    for item in owm.forecast_at_place(city, "3h").forecast:  # Sorting through weather data
        weather_at_place_3h.append(item)

    return cast_to_days(weather_at_place_3h)  # Calling Func cast_to_days  to frame the data


def cast_to_days(data):  # Introduction of a function for framing data
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

        if times != 0:
            day.temperature('celsius')['temp'] /= times  # Finding the average temperature
            new_data.append(day)  # Filling an array with data

    return new_data  # Output of an array with data


def print_weather(data):  # Func for output data
    ref_time = datetime.datetime.fromtimestamp(data.ref_time).strftime('%Y-%m-%d %H:%M')
    print(f"Time\t\t: {ref_time}")
    print(f"Temperature\t: {data.temperature('celsius')['temp']}")
    if data.rain:
        print(f"Rain: true")
    print("\n")


def day_to_num(day):  # Function for numbering days
    lower_day = day.lower()

    if lower_day == "today":
        return datetime.date.today().weekday()

    if lower_day == "mo":
        return 0

    if lower_day == "tu":
        return 1

    if lower_day == "we":
        return 2

    if lower_day == "th":
        return 3

    if lower_day == "fr":
        return 4

    if lower_day == "sa":
        return 5

    if lower_day == "sun":
        return 6

    return 0


if __name__ == '__main__':
    if args.day_parser == "week":
        get_weather()  # Calling the function with the weather for 5 days

    if args.day_parser == "today":
        get_day_weather(args.day_value, "***Current day weather***")  # Calling a function with weather data for today

    if args.day_parser == "mo" or args.day_value == "tu" or args.day_value == "we" or args.day_value == "th" or args.day_value == "fr" or args.day_value == "sa" or args.day_value == "sun":
        get_day_weather(args.day_value,"***Certain day weather***")  # Calling a function with weather data on a specific day









