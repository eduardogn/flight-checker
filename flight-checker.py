import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Function to get the cheapest flight price from Porto to Wroclaw
def get_cheapest_flight_price(from_city, to_city):
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/PT/EUR/en-US/" + from_city + "/" + to_city + "/anytime"

    headers = {
        "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "219b221a3fmsha9763c52a9a6d6fp1e986djsn6772c106a918"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # Get the cheapest price from the response
    cheapest_price = data["MinPrice"]

    return cheapest_price

# Function to update the Google Sheet with the data
def update_google_sheet(datetime, carrier, flight_day_and_time, flight_price_in_euros):
    # Authenticate to Google Sheets API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("nodal-operand-376812-7ff1deb55dbe.json", scope)
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open("flight-checker-app").sheet1

    # Append the data to the sheet
    sheet.append_row([datetime, carrier, flight_day_and_time, flight_price_in_euros])

# Main program logic
if __name__ == "__main__":
    while True:
        # Get the cheapest flight price
        price = get_cheapest_flight_price("OPO", "WRO")

        # Get the current date and time
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")

        # Update the Google Sheet with the data
        update_google_sheet(date, "<flight-carrier>", time, price)

        # Wait for 1 hour before checking again
        time.sleep(360)
