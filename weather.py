import schedule
import time
import requests
from twilio.rest import Client

def get_weather(latitude, longitude):
    # Fetch the current weather data from Open-Meteo API for the given latitude and longitude
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
    response = requests.get(base_url)
    data = response.json()
    return data

def celsius_to_fehrinheit(celsius):
    # Convert temperature from Celsius to Fahrenheit
    return (celsius * 9/5) + 32

def send_text_message(body):
    # Send a text message using Twilio API
    account_sid = "twilio_sid"  # Replace with your Twilio SID
    auth_token = "twilio_token"  # Replace with your Twilio Auth Token
    from_phone_number = "from_phone_number"  # Replace with your Twilio phone number
    to_phone_number = "to_phone_number"  # Replace with the phone number to send message

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=from_phone_number,
        to=to_phone_number
    )
    print("Text message sent!")

def send_weather_update():
    # Prepare and send the weather update text message
    # Hardcoded location for NYC
    latitude = 40.7128
    longitude = -74.0060

    # Get weather data for NYC
    weather_data = get_weather(latitude, longitude)
    temp_celsius = weather_data["hourly"]["temperature_2m"][0]
    relative_humidity = weather_data["hourly"]["humidity_2m"][0]
    wind_speed = weather_data["hourly"]["windspeed_10m"][0]
    temp_fahrenheit = celsius_to_fehrinheit(temp_celsius)

    # Format the weather information
    weather_info = (
        f"Good Morning! Here's the current weather in NYC:\n"
        f"Temperature: {temp_fahrenheit}°F\n"
        f"Relative Humidity: {relative_humidity}%\n"
        f"Wind Speed: {wind_speed} m/s"
    )

    # Send the formatted weather information as a text message
    send_text_message(weather_info)

def main():
    # Schedule the weather update message to be sent every day at 8:00 AM
    schedule.every().day.at("08:00").do(send_weather_update)

    # Run the scheduler in an infinite loop
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()  # Entry point of the program
