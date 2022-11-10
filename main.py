# Import all the essential Module for SMS Weather Aleart project
import requests # Request Module is used to get API request in python
from twilio.rest import Client # Twilio Module is used to get Virtual Number and sent SMS on any Verified Twilio number
import os # This Module is used to Secure/Hide API key (To change environment variable)

# You can get auth_token and account_sid by signup in https://www.twilio.com/
account_sid = os.environ.get("OVM_Api_Key")
auth_token = os.environ.get("OVM_Auth")

# This is open weather map url from which we get information about Weather
url = "https://api.openweathermap.org/data/2.5/forecast?"

# You can get open weather map api key by signup in https://openweathermap.org/
api_key = os.environ.get("OWF_api_key")

# This is the required parameter you have to set to request weather information from openweathermap
params = {
    "lat": "Your_Latitude",
    "lon": "Your_Longitute",
    "appid": api_key,
}
# Here getting information about "5 day / 3 hour forecast data"
response = requests.get(url, params=params)
response.raise_for_status()
weather_data = response.json()["list"]
will_rain = False
weather_description = []
# Here Converting 5 days weather information in one day weather information by slicing data
# You can use json online Viewer to see data in good format
for hourly in weather_data[:11]:
    description = hourly['weather'][0]['description']
    id = hourly["weather"][0]["id"] # If ID is bellow 700 which means rain, snow, thunderstorm and more etc
    if id<=700:
        will_rain = True
    if description not in weather_description:
        weather_description.append(description)
# Here using twilio to get sms about weather
# You can read twilio sms api docs to better understand this from here https://www.twilio.com/docs/sms/quickstart/python
# Here sending sms to my number about whether to take umbrella or not and also weather description
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"Bring an Umbrella ☂️and Today weather Description {weather_description}",
        from_='Twilio_Number',
        to='Your_Number'
    )
else:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"You're clear to go and Today weather Description {weather_description}",
        from_='Twilio_Number',
        to='Your_Number'
    )

# Here printing message status sms send successfully or not
print(message.status)


