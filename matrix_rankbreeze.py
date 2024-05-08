import os
import time
from selenium import webdriver
import shutil
from selenium.common.exceptions import NoSuchElementException
import datetime
import pytz
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

# Google Sheets setup
SHEET_ID = '1RG-5uy_k3GbpDYINKDAZLh0UomU3U41N-Pk50Qtaus8'
SHEET_NAME = 'Data'
SHEET_NAME2 = 'impressions'
SHEET_NAME3 = 'click'
SHEET_NAME4 = 'listing_v'
SHEET_NAME5 = 'conversion_r'
SHEET_NAME6 = 'lead_times'
SHEET_NAME7 = 'abnb_occu'
SHEET_NAME8 = 'daily_rates'
SHEET_NAME9 = 'revenue'

# Get Google Sheets credentials from environment variable
GSHEET_CRED_MATRIX_RBREEZE = os.getenv("GSHEET_CRED_MATRIX_RBREEZE")
credentials = Credentials.from_service_account_info(json.loads(GSHEET_CRED_MATRIX_RBREEZE))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

eastern_tz = pytz.timezone("America/New_York")
current_time = datetime.datetime.now(eastern_tz)

username = "Marketing@novavacation.com"
passw = "Novabookings@2024!"

website = "https://app.rankbreeze.com/listings"

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
driver.get(website)

time.sleep(2)

driver.find_element("xpath", """(//div[@class="form-group"]/input)[1]""").send_keys(username)
time.sleep(2)
driver.find_element("xpath", """(//div[@class="form-group"]/input)[2]""").send_keys(passw)
log = driver.find_element("xpath", """(//div[@class="form-group"]/input)[3]""")
time.sleep(2)
log.click()
time.sleep(4)  # 20

proxy_links = ["https://app.rankbreeze.com/rankings/70468",
              "https://app.rankbreeze.com/rankings/70467",
              "https://app.rankbreeze.com/rankings/70466",
              "https://app.rankbreeze.com/rankings/70465",
              "https://app.rankbreeze.com/rankings/70464",
              "https://app.rankbreeze.com/rankings/70463",
              "https://app.rankbreeze.com/rankings/70462",
              "https://app.rankbreeze.com/rankings/70461",
              "https://app.rankbreeze.com/rankings/70460",
              "https://app.rankbreeze.com/rankings/70459", ]

data = []
overall_impressions = []
overall_search_conversion_rate = []
overall_listing_views = []
overall_conversion_rate = []
overall_lead_times = []
overall_airbnb_occupancy = []
overall_avg_daily_rates = []
overall_revenue = []

for website in proxy_links:
    driver.get(website)
    time.sleep(4)

    driver.get(website)

    time.sleep(3)

    link = website

    link_Id = website.strip("https://app.rankbreeze.com/rankings/")

    proxy_title = driver.find_element("xpath", """//*[@id="get-email"]/div/main/div[3]/div[1]/h2""").get_attribute(
        "innerText")

    guest_satisfaction = driver.find_element("xpath", """(//div[@class="single-value"]/b)[1]""").get_attribute(
        "innerText")

    reviews_count = driver.find_element("xpath", """(//div[@class="single-value"]/b)[2]""").get_attribute("innerText")

    date_str = current_time.strftime("%Y-%m-%d")  # 'YYYY-MM-DD'

    date_hours_str = current_time.strftime("%Y-%m-%d %H:%M:%S")  # 'YYYY-MM-DD HH:MM:SS


    # Define the function to extract table data
    def extract_table_data(rows, num_columns):
        table_data = []
        for row in rows:
            columns = row.find_elements("xpath", "./td")
            if len(columns) >= num_columns:
                column_texts = [column.get_attribute("innerText").strip() for column in columns[:num_columns]]

                if constant_values:
                    column_texts.extend(constant_values)

                table_data.append(tuple(column_texts))
        return table_data


    # Find and extract data for impressions and search conversion rate
    impressions = driver.find_elements("xpath", """//*[@id="first_page_search_impressions"]//tbody/tr""")
    search_conversion_rate = driver.find_elements("xpath", """//*[@id="search_conversion_rate"]//tbody/tr""")

    listing_views = driver.find_elements("xpath", """//*[@id="page_views"]//tbody/tr""")
    conversion_rate = driver.find_elements("xpath", """//*[@id="conversion_rate"]//tbody/tr""")
    lead_times = driver.find_elements("xpath", """//*[@id="booking_lead_time"]//tbody/tr""")
    airbnb_occupancy = driver.find_elements("xpath", """//*[@id="occupancy_rate"]//tbody/tr""")
    avg_daily_rates = driver.find_elements("xpath", """//*[@id="average_daily_rate"]//tbody/tr""")
    revenue = driver.find_elements("xpath", """//*[@id="revenue"]//tbody/tr""")

    constant_values = [link, link_Id, proxy_title, date_str, date_hours_str]

    # Store extracted data in respective overall lists
    overall_impressions.extend(extract_table_data(impressions, 3))
    overall_search_conversion_rate.extend(extract_table_data(search_conversion_rate, 3))
    overall_listing_views.extend(extract_table_data(listing_views, 3))
    overall_conversion_rate.extend(extract_table_data(conversion_rate, 3))
    overall_lead_times.extend(extract_table_data(lead_times, 3))
    overall_airbnb_occupancy.extend(extract_table_data(airbnb_occupancy, 3))
    overall_avg_daily_rates.extend(extract_table_data(avg_daily_rates, 3))
    overall_revenue.extend(extract_table_data(revenue, 2))

    data.append({
        "Link": link,
        "Link Id": link_Id,
        "Rental Name": proxy_title,
        "Reviews Count": guest_satisfaction,
        "Star Reviews": reviews_count,
        "Date Gathered": date_str,
        "Date Gathered Hours": date_hours_str,
    })

# Append `data` to 'Data' sheet
try:
    # Convert `data` to a list of lists for Google Sheets
    values = [list(d.values()) for d in data]

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=SHEET_NAME,  # 'Data' sheet
        valueInputOption="RAW",
        body={"values": values},
    ).execute()
except HttpError as e:
    print("Error appending data to 'Data' sheet in Google Sheets:", e)

# Append `overall_impressions` to 'impressions' sheet
try:
    # Convert `overall_impressions` to a list of lists
    values2 = list(overall_impressions)

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=SHEET_NAME2,  # 'impressions' sheet
        valueInputOption="RAW",
        body={"values": values2},
    ).execute()
except HttpError as e:
    print("Error appending data to 'impressions' sheet in Google Sheets:", e)

try:

    values3 = list(overall_search_conversion_rate)

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=SHEET_NAME3,  # 'impressions' sheet
        valueInputOption="RAW",
        body={"values": values3},
    ).execute()
except HttpError as e:
    print("Error appending data to 'click' sheet in Google Sheets:", e)

try:

    values4 = list(overall_listing_views)

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=SHEET_NAME4,  # 'impressions' sheet
        valueInputOption="RAW",
        body={"values": values4},
    ).execute()
except HttpError as e:
    print("Error appending data to 'listing_v' sheet in Google Sheets:", e)

try:

    values5 = list(overall_conversion_rate)

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=SHEET_NAME5,  # 'impressions' sheet
        valueInputOption="RAW",
        body={"values": values5},
    ).execute()
except HttpError as e:
    print("Error appending data to 'conversion_r' sheet in Google Sheets:", e)

try:

    values6 = list(overall_lead_times)

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=SHEET_NAME6,  # 'impressions' sheet
        valueInputOption="RAW",
        body={"values": values6},
    ).execute()
except HttpError as e:
    print("Error appending data to 'lead_times' sheet in Google Sheets:", e)

try:

    values7 = list(overall_airbnb_occupancy)

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=SHEET_NAME7,  # 'impressions' sheet
        valueInputOption="RAW",
        body={"values": values7},
    ).execute()
except HttpError as e:
    print("Error appending data to 'abnb_occu' sheet in Google Sheets:", e)

try:

    values8 = list(overall_avg_daily_rates)

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=SHEET_NAME8,  # 'impressions' sheet
        valueInputOption="RAW",
        body={"values": values8},
    ).execute()
except HttpError as e:
    print("Error appending data to 'daily_rates' sheet in Google Sheets:", e)

try:

    values9 = list(overall_revenue)

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=SHEET_NAME9,  # 'impressions' sheet
        valueInputOption="RAW",
        body={"values": values9},
    ).execute()
except HttpError as e:
    print("Error appending data to 'revenue' sheet in Google Sheets:", e)

