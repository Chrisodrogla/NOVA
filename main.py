import pandas as pd
import time
from selenium import webdriver
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import json

# Set up Chrome WebDriver with custom options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

# Google Sheets setup
SHEET_ID = '1Y-h3p_iHqvOXRkM1opCzo6tlCOM1mLzbaOJ57VnaFU8'  
SHEET_NAME = 'Sheet1' 

# Get Google Sheets credentials from environment variable
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

# Get the list of existing website links
existing_websites = [row[6] for row in existing_data[1:]]  

# List of websites to scrape
link_websites = [
'https://www.airbnb.com/rooms/618297070744530980?adults=1&category_tag=Tag%3A8188&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1393757704&check_in=2024-12-01&check_out=2024-12-06&source_impression_id=p3_1714964601_g0rZVSVpYhYqRXk1&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD',
 'https://www.airbnb.com/rooms/28254684?adults=1&category_tag=Tag%3A8528&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1838474145&check_in=2024-05-10&check_out=2024-05-15&source_impression_id=p3_1714964602_hpdXE4TeZSCuxUvp&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD',
'https://www.airbnb.com/rooms/884326009163810236?adults=1&category_tag=Tag%3A677&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1644195432&check_in=2024-05-26&check_out=2024-05-31&source_impression_id=p3_1714964602_HNn4UT3hlEkuxfqy&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD',
 'https://www.airbnb.com/rooms/883292961768197366?adults=1&category_tag=Tag%3A4104&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1642901295&check_in=2024-05-26&check_out=2024-05-31&source_impression_id=p3_1714964603_3m2Y2iGdSoOjT2r6&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD',
 'https://www.airbnb.com/rooms/945067261594664496?adults=1&category_tag=Tag%3A5348&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1724006574&check_in=2024-06-16&check_out=2024-06-21&source_impression_id=p3_1714964603_Bb1%2F6D0v4FPBi78%2F&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD',
 'https://www.airbnb.com/rooms/46711243?adults=1&category_tag=Tag%3A8225&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1101555283&check_in=2024-06-26&check_out=2024-07-01&source_impression_id=p3_1714964603_Aa%2F3zUSufLI1nko8&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD',
 'https://www.airbnb.com/rooms/44119404?adults=1&category_tag=Tag%3A8188&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1046530861&check_in=2024-11-03&check_out=2024-11-08&source_impression_id=p3_1714964603_dqtdBaezFIfS%2BmXm&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD',
 'https://www.airbnb.com/rooms/49797626?adults=1&category_tag=Tag%3A8225&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1805824477&check_in=2024-05-06&check_out=2024-05-11&source_impression_id=p3_1714964603_Sui7PpbmykGpi6O6&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD',
 'https://www.airbnb.com/rooms/1102694040249896667?adults=1&category_tag=Tag%3A8186&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1851766802&check_in=2024-05-13&check_out=2024-05-18&source_impression_id=p3_1714964603_CW06I2GqRQMOp5WC&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD',
 'https://www.airbnb.com/rooms/613149034120950698?adults=1&category_tag=Tag%3A677&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1388900672&check_in=2024-05-27&check_out=2024-06-01&source_impression_id=p3_1714964603_VszbIk2L1azbUuqj&previous_page_section_name=1000&federated_search_id=a7b05e53-37a9-4366-8067-dde27a88e972&currency=USD',


]

data = []

# Loop through the websites and collect data
for website in link_websites:
    if website not in existing_websites:  # this wll skip if the website already exists on the gsheet
        driver = webdriver.Chrome(options=options)
        driver.get(website)
        time.sleep(2)

        # Xpaths
        address_name = driver.find_element("xpath", """//div[@style="display: contents;"]/section/div/h2""").get_attribute("innerText")
            
        price = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[1]""").get_attribute("innerText") 
        
        guest_bed_bath = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol""").text
        
        reviews_count = driver.find_element("xpath", """//span[@class="_1wl1dfc"] | //span[@class="_17qqrnq"]""").get_attribute("innerText").strip(" reviews")
        
        star_reviews = driver.find_element("xpath", """//span[@class="_12si43g"]""").get_attribute("innerText").strip(" ·")
        
        hosted_by = driver.find_element("xpath", """//div[@class="t1pxe1a4 atm_c8_2x1prs atm_g3_1jbyh58 atm_fr_11a07z3 atm_cs_9dzvea dir dir-ltr"]""").get_attribute("innerText")
    
        # Add to the data list
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

# Convert the data to Df
df = pd.DataFrame(data)

# Append the new data Gsheet avoiding duplicates
if not df.empty:
    # Convert DataFrame to list of lists for Google Sheets
    values = df.values.tolist()

    
    try:
        service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=SHEET_NAME,  
            valueInputOption="RAW",
            body={"values": values},
        ).execute()
    except HttpError as e:
        print("Error appending data to Google Sheets:", e)
