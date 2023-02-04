Python app:

import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Skyscanner API endpoint for flight prices
endpoint = "http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/{country}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={api_key}"

# Replace with your Skyscanner API key
api_key = "your_api_key"

# Replace with your origin and destination
originPlace = "OPO-sky"
destinationPlace = "WRO-sky"

# Replace with your country, currency and locale
country = "PT"
currency = "EUR"
locale = "pt-PT"

# Replace with your desired outbound and inbound dates
outboundPartialDate = "anytime"
inboundPartialDate = "anytime"

# Construct the URL for the API request
url = endpoint.format(country=country, currency=currency, locale=locale, 
                      originPlace=originPlace, destinationPlace=destinationPlace, 
                      outboundPartialDate=outboundPartialDate, inboundPartialDate=inboundPartialDate, api_key=api_key)

# Make the API request
response = requests.get(url)

# Parse the JSON response
data = response.json()

# Get the first result (cheapest flight)
flight = data["Quotes"][0]

# Get the flight carrier
carrier = data["Carriers"][0]["Name"]

# Get the flight date
date = data["Quotes"][0]["OutboundLeg"]["DepartureDate"]

# Get the flight price
price = data["Quotes"][0]["MinPrice"]

# Connect to Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("Skyscanner Flights").sheet1

# Get the current date and time
now = datetime.datetime.now()

# Append the new data to the Google Sheet
sheet.append_row([now, carrier, date, price])