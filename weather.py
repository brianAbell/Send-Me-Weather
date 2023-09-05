import schedule
import time
import requests
from twilio.rest import Client



def get_weather(latitude, longitude):
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude=40.7143&longitude=-74.006&hourly=temperature_2m"
    response = requests.get(base_url)
    data = response.json()
    return data

def celsius_to_fehrinheit(celsius):
    return (celsius * 9/5) + 32

def send_text_message(body):
    account_sid = "twilio_sid"
    auth_token = "twilio_token"
    from_phone_number = "from_phone_number"
    to_phone_number = "to_phone_number"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body = body,
        from_ = from_phone_number,
        to = to_phone_number
    )
    print("Text message sent!")


def send_weather_update():
    #hardcoded location for NYC
    latitude = 40.7128
    longitude = -74.0060

    weather_data = get_weather(latitude, longitude)
    temp_celsius = weather_data["hourly"]["temperature_2"][0]
    relative_humidity = weather_data["hourly"]["humidity_2m"][0]
    wind_speed = weather_data["hourly"]["windspeed_10m"][0]
    temp_fahrenheit = celsius_to_fehrinheit(temp_celsius)

    weather_info = (
        f"Good Morning Brian!\n"
        f"Current Weather in NYC:\n"
        f"Temperature: {temp_fahrenheit}\n"
        f"Relative Humidity: {relative_humidity}\n"
        f"Wind Speed: {wind_speed} m/s"
    )

    send_text_message(weather_info)



def main():
    schedule.every().day.at("08:00").do(send_weather_update)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__== "__main__":
    main()
