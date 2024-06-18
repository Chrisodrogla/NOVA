import pandas as pd
from datetime import date
import time
from selenium import webdriver
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import json

# Set up Chrome WebDriver with custom options
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

# Google Sheets setup
SHEET_ID = '1Y-h3p_iHqvOXRkM1opCzo6tlCOM1mLzbaOJ57VnaFU8'
SHEET_NAME1 = 'Sheet1'  # Sheet to clear
SHEET_NAME2 = 'Sheet2'  # Sheet to append

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Delete all rows in Sheet1 (if it exists)
try:
    service.spreadsheets().values().clear(spreadsheetId=SHEET_ID, range=SHEET_NAME1).execute()
except HttpError as e:
    print("Error clearing data from Sheet1:", e)

# Read existing data from Google Sheets to avoid duplicates in Sheet2
try:
    response = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=SHEET_NAME2).execute()
    existing_data = response.get("values", [])
except HttpError as e:
    print("Error fetching data from Sheet2:", e)
    existing_data = []

# Get the list of existing website links from Sheet2
existing_websites = [row[6] for row in existing_data[1:]]  # Assuming website URL is in the 7th column (index 6)

# List of websites to scrape
link_websites = [
    'https://www.airbnb.com/rooms/7146166',
    'https://www.airbnb.com/rooms/796474546246084466',
    'https://www.airbnb.com/rooms/37941371',
    # Add more URLs as needed
]

DateToday = date.today()
UpdatedAt = DateToday.strftime("%Y-%m-%d")

data = []
for website in link_websites:
    driver = webdriver.Chrome(options=options)
    driver.get(website)
    
    time.sleep(3)
    try:
        click_x = driver.find_element("xpath", """/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button""").click()
    except:
        pass
    
    try:
        listing_id = website.split('/')[-1]
    except:
        listing_id = "N/A"

    try:
        review_counts = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div[1]/div[2]/span/span[3]""").get_attribute("innerText").strip(' reviews')
    except:
        review_counts = ""

    try:
        guest_bed_bath = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol""").text
    except:
        guest_bed_bath = "N/A"

    try:
        reviews_count = driver.find_element("xpath", """//span[@class="_1wl1dfc"] | //span[@class="_17qqrnq"]""").get_attribute("innerText").strip(" reviews")
    except:
        reviews_count = "N/A"

    try:
        AirbnbBadge1 = driver.find_element("xpath", """//div[@data-plugin-in-point-id='GUEST_FAVORITE_BANNER']""")
        if AirbnbBadge1:
            AirbnbBadge = "Guest favorite"
        else:
            AirbnbBadge = "Guest favorite"
    except:
        AirbnbBadge = ''
            
    try:
        star_reviews = driver.find_element("xpath", """//span[@class="_12si43g"]""").get_attribute("innerText").strip(" ·")
    except:
        star_reviews = "N/A"

    try:
        hosted_by = driver.find_element("xpath", """//div[@class="t1pxe1a4 atm_c8_2x1prs atm_g3_1jbyh58 atm_fr_11a07z3 atm_cs_9dzvea dir dir-ltr"]""").get_attribute("innerText").strip('Hosted by')
    except:
        hosted_by = "N/A"

    try:
        CohostName = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/section/div[2]/div/div/div[2]/div[1]/ul/li[1]/span""").get_attribute("innerText")
    except:
        CohostName = ""
    try:
        Cohost2nd = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/section/div[2]/div/div/div[2]/div[1]/ul/li[2]/span""").get_attribute("innerText")
    except:
        Cohost2nd = ""
        
    try:
        Cleanliness = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div/div[2]/div[2]""").get_attribute("innerText")
        Accuracy = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[3]/div/div/div[2]/div[2]""").get_attribute("innerText")
        Checkin = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[4]/div/div/div[2]/div[2]""").get_attribute("innerText")
        Communication = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[5]/div/div/div[2]/div[2]""").get_attribute("innerText")
        Location = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[6]/div/div/div[2]/div[2]""").get_attribute("innerText")
        Value = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[7]/div/div/div[2]/div[2]""").get_attribute("innerText")
    except:
        Cleanliness = ''
        Accuracy = ''
        Checkin = ''
        Communication = ''
        Location = ''
        Value = ''
        
    try:
        Title = driver.find_element("xpath", """//div[@data-plugin-in-point-id="TITLE_DEFAULT"]//h1""").get_attribute("innerText")
    except:
        Title = ""
 
    try:
        ResponseRate = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/section/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]""").text
        ResponseTime = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/section/div[2]/div/div/div[2]/div[2]/div/div[2]/div[2]""").text
        LastReviewName = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[3]/div/div/div[1]//h3""").get_attribute("innerText")
        LastReviewStar = driver.find_element("xpath", """(//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[3]/div/div/div[1]//span)[1]""").get_attribute("innerText")
    except:
        ResponseRate = ""
        ResponseTime = ""
        LastReviewName = ""
        LastReviewStar = ""

    driver.quit()

    data.append({
        "Listing ID": listing_id,
        "Star Reviews": star_reviews,
        "ReviewNumber": review_counts,
        "AirbnbBadge": AirbnbBadge,
        "MainHost": hosted_by,
        "CohostName": CohostName,
        "Cohost2nd": Cohost2nd,
        "Original_URL": website,
        "Cleanliness": Cleanliness,
        "Accuracy": Accuracy,
        "Checkin": Checkin,
        "Communication": Communication,
        "Location": Location,
        "Value": Value,
        "Title": Title,
        "ResponseRate": ResponseRate,
        "ResponseTime": ResponseTime,
        "LastReviewName": LastReviewName,
        "LastReviewStar": LastReviewStar,
        "UpdatedAt": UpdatedAt,
    })

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Append the new data to Sheet2, avoiding duplicates
if not df.empty:
    # Convert DataFrame to list of lists for Google Sheets
    values = df.values.tolist()

    try:
        service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=SHEET_NAME2,
            valueInputOption="RAW",
            body={"values": values},
        ).execute()
        print("Data appended to Sheet2 successfully.")
    except HttpError as e:
        print("Error appending data to Sheet2:", e)
else:
    print("DataFrame is empty, no data to append.")

