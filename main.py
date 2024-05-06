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
'https://www.airbnb.com/rooms/618297070744530980?adults=1&category_tag=Tag%3A8188&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1393757704&check_in=2024-12-01&check_out=2024-12-06&source_impression_id=p3_1714964601_g0rZVSVpYhYqRXk1&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD',
 'https://www.airbnb.com/rooms/28254684?adults=1&category_tag=Tag%3A8528&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1838474145&check_in=2024-05-10&check_out=2024-05-15&source_impression_id=p3_1714964602_hpdXE4TeZSCuxUvp&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD'
]

data = []
for website in link_websites1:
    if website in existing_urls:
        continue  # Skip if the website is already in the sheet

    driver = webdriver.Chrome(options=options)
    driver.get(website)

    time.sleep(2)

    address_name = driver.find_element("xpath", """//div[@style="display: contents;"]/section/div/h2""").get_attribute("innerText")
    
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
