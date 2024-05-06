import os
import gspread
from google.oauth2.service_account import Credentials

# Get credentials from environment
credentials_dict = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
creds = Credentials.from_service_account_info(eval(credentials_dict))

# Connect to Google Sheets
client = gspread.authorize(creds)

# Open a known Google Sheet
sheet = client.open("Airbnb-sample-scraper").worksheet("Sheet1")

# Fetch a simple value to test the connection
cell_value = sheet.acell("A1").value
print("Value in A1:", cell_value)
