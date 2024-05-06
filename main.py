import os
import time
import pandas as pd
from selenium import webdriver
from google.oauth2.service_account import Credentials
import gspread

# Set up Chrome WebDriver with custom download directory
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920x1080")

# Google Sheets setup
credentials_dict = os.getenv("GOOGLE_SHEETS_CREDENTIALS")  # Get credentials from env
creds = Credentials.from_service_account_info(eval(credentials_dict))  # Parse as JSON

client = gspread.authorize(creds)  # Authorize
sheet = client.open("Airbnb-sample-scraper").worksheet("Sheet1")  # Change to your sheet name

# Get existing website URLs to avoid duplicates
existing_urls = sheet.col_values(3)  # Assuming 'Web_Link' is in the 3rd column

# List of websites to scrape
link_websites1 = [
    'https://www.airbnb.com/rooms/618297070744530980?adults=1...',
    'https://www.airbnb.com/rooms/28254684?adults=1...',
]

data = []
for website in link_websites1:
    if website in existing_urls:
        continue  # Skip if the website is already in the sheet

    driver = webdriver.Chrome(options=options)
    driver.get(website)

    time.sleep(2)

    address_name = driver.find_element("xpath", """//div[@style="display: contents;"]/section/div/h2""").get_attribute(
        "innerText")

    data.append({
        "Address": address_name,
        "Web_Link": website,
    })

    driver.quit()

if data:
    df = pd.DataFrame(data)

    # Append new data to Google Sheets
    for _, row in df.iterrows():
        sheet.append_row([row["Address"], None, row["Web_Link"]])  # Adjust for your columns
else:
    print("No new data to add.")
