import pandas as pd
import time
from selenium import webdriver
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up Chrome WebDriver with custom options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

# Google Sheets setup
SHEET_ID = '1Y-h3p_iHqvOXRkM1opCzo6tlCOM1mLzbaOJ57VnaFU8' # Add your Google Sheet ID here
SHEET_NAME = 'Sheet1' # Change to your sheet name if needed

# Get Google Sheets credentials from the environment variable
import os
import json
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Read existing data from Google Sheets to avoid duplicates
try:
    response = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=SHEET_NAME).execute()
    existing_data = response.get("values", [])
except HttpError as e:
    print("Error fetching data from Google Sheets:", e)
    existing_data = []

# Get the list of existing websites
existing_websites = [row[6] for row in existing_data[1:]]  # Assuming column 7 contains the website links

# List of websites to scrape
link_websites = [
    'https://www.airbnb.com/rooms/618297070744530980?adults=1&category_tag=Tag%3A8188&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1393757704&check_in=2024-12-01&check_out=2024-12-06',
    'https://www.airbnb.com/rooms/28254684?adults=1&category_tag=Tag%3A8528&children=0&enable_m3_private_room=true&infants=0&pets=0&check_in=2024-05-10&check_out=2024-05-15',
]

data = []

# Loop through the websites and collect data
for website in link_websites:
    if website not in existing_websites:  # Skip if the website already exists in Google Sheets
        driver = webdriver.Chrome(options=options)
        driver.get(website)
        time.sleep(2)

        # Extract information
        address_name = driver.find_element("xpath", "//div[@style='display: contents;']/section/div/h2").get_attribute("innerText")
        price = driver.find_element("xpath", "//span[@data-element-name='description']").get_attribute("innerText")
        guest_bed_bath = driver.find_element("xpath", "//ol").text
        reviews_count = driver.find_element("xpath", "//span[@class='_1wl1dfc'] | //span[@class='_17qqrnq']").get_attribute("innerText").strip(" reviews")
        star_reviews = driver.find_element("xpath", "//span[@class='_12si43g']").get_attribute("innerText").strip(" ·")
        hosted_by = driver.find_element("xpath", "//div[@class='t1pxe1a4 atm_c8_2x1prs atm_g3_1jbyh58 atm_fr_11a07z3 atm_cs_9dzvea dir dir-ltr']").get_attribute("innerText")

        # Add to data list
        data.append({
            "Address": address_name,
            "Price": price,
            "Guest/Bed/Bath": guest_bed_bath,
            "Reviews Count": reviews_count,
            "Star Reviews": star_reviews,
            "Hosted By": hosted_by,
            "Web_Link": website,
        })
        
        driver.quit()

# Convert data to DataFrame
df = pd.DataFrame(data)

# Append the new data to Google Sheets
if not df.empty:
    # Convert DataFrame to list of lists for Google Sheets
    values = df.values.tolist()

    # Append data to Google Sheets
    try:
        service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=SHEET_NAME,
            valueInputOption="RAW",
            body={"values": values},
        ).execute()
    except HttpError as e:
        print("Error appending data to Google Sheets:", e)
