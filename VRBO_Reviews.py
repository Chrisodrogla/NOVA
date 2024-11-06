################# SCRAPER ###########################

import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from datetime import date
import time
from selenium import webdriver
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import json


# Set up Chrome WebDriver with options
options = webdriver.ChromeOptions()
# Add additional options to use the display created by Xvfb
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--start-maximized")  # Set display to Xvfb


UpdatedAt = datetime.datetime.now().strftime('%m/%d/%Y')

# # Open and read the file
# with open('List_VRBO_Listings.txt', 'r') as file:
#     # Read each line, strip any whitespace, and store in a list
#     Links_IDS = [line.strip() for line in file if line.strip()]
#
# # Initialize an empty list to store the modified links
# Links = []
#
# # Loop through each ID and create the modified link
# for ID in Links_IDS:
#     Link_modified = "https://www.vrbo.com/" + ID
#     Links.append(Link_modified)

# Sample Links
Links = \
    ["https://www.vrbo.com/7727993ha",
    "https://www.vrbo.com/7069423ha"]

driver = webdriver.Chrome(options=options)
data = []

for Link in Links:
    driver.get(Link)
    time.sleep(5)
    driver.execute_script("document.body.style.zoom='25%'")
    #     driver.execute_script("document.body.style.zoom='70%'")
    try:
        Reviews_Button = driver.find_element("xpath",
                                             """//div[@class="uitk-layout-flex-item"]//button[contains(text(), 'See')]""")

    except:
        continue

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", Reviews_Button)
    time.sleep(1)
    Reviews_Button.click()

    time.sleep(3)
    # Loop to keep clicking "More reviews" until there are no more buttons
    while True:
        try:
            # Locate the "More reviews" button
            Load_More = driver.find_element("xpath", """//button[contains(text(), 'More reviews')]""")

            # Scroll to the button to ensure it's in view
            Load_More.send_keys(Keys.END)
            time.sleep(2)  # Small pause to allow page to load new content

            # Click the button
            Load_More.click()
            time.sleep(2)  # Pause to allow more reviews to load

        except:

            break

    Reviews = driver.find_elements("xpath",
                                   """//div[@class="uitk-card uitk-card-roundcorner-all uitk-card-has-primary-theme"]/div""")

    for Review in Reviews:

        Link_ID = Link.split('com/')[1].strip("ha")

        Link = Link
        try:
            Rating = Review.find_element("xpath", """.//h3[@class="uitk-heading uitk-heading-5"]""").text
        except:
            Rating = ""
        try:    
            GuestName = Review.find_element("xpath", """.//h4""").text
        except:
            GuestName = ""
        try:     
            Date = Review.find_element("xpath", """.//span[@itemprop="datePublished"]""").text
        except:
            Date = ""
        try:
            Standard = Review.find_element("xpath",
                                           """.//section[contains(@class, 'uitk-spacing') and .//span[contains(text(), 'Like')]]""").text
        except:
            Standard = ""
        try:
            Content = Review.find_element("xpath", """.//span[@itemprop="description"]""").text
        except:
            Content = ""
        try:
            Stayed = Review.find_element("xpath", """.//div[contains(text(), 'Stayed')]""").text
        except:
            Stayed = ""
        try:
            Response_Content = Review.find_element("xpath",
                                                   """.//article[descendant::text()[contains(., 'Response from VrboOwner on')]]//section[2]""").text
        except:
            Response_Content = ""

        try:
            Response_Date = Review.find_element("xpath",
                                                """.//article[descendant::text()[contains(., 'Response from VrboOwner on')]]//section[1]""").text.strip(
                'Response from VrboOwner on')
        except:
            Response_Date = ""

        row_data = {

            "Link_ID": Link_ID,
            "Rating": Rating,
            "Standard": Standard,
            "GuestName": GuestName,
            "Date": Date,
            "Content": Content,
            "Response_Content": Response_Content,
            "Response_Date": Response_Date,
            "Stayed": Stayed,
            "Link": Link,
            "UpdatedAt": UpdatedAt
        }
        data.append(row_data)

driver.quit()

# Create a DataFrame with the data
df = pd.DataFrame(data)



# Google Sheets setup
SHEET_ID = '1S6gAIsjuYyGtOmWFGpF9okAPMWq6SnZ1zbIylBZqCt4'
SHEET_NAME1 = 'VRBO_reviews'  # Sheet to clear data below header and write new data

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)


# Clear all data below header in the "Review" sheet
service.spreadsheets().values().clear(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME1}!A2:Z"
).execute()

# Write new data to the "Review" sheet starting from row 2
service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME1}!A2",
    valueInputOption="RAW",
    body={"values": df.values.tolist()}
).execute()
