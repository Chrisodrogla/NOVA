import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import json

# Google Sheets setup
SHEET_ID = '1RG-5uy_k3GbpDYINKDAZLh0UomU3U41N-Pk50Qtaus8'
SHEET_NAME = 'Data'
SHEET_NAME2 = 'impressions'

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GSHEET_CRED_MATRIX_RBREEZE")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Data to append
data = [
    {
        'Link': 'https://app.rankbreeze.com/rankings/71585',
        'Link Id': '71585',
        'Rental Name': 'Windsor Island Resort 5br Villa Pool near Disney',
        'Reviews Count': '87.0',
        'Star Reviews': '33',
        'Date Gathered': '2024-05-08',
        'Date Gathered Hours': '2024-05-08 08:27:29'
    },
    {
        'Link': 'https://app.rankbreeze.com/rankings/71572',
        'Link Id': '71572',
        'Rental Name': 'Listing #1146531341370055903 unlisted or no longer available',
        'Reviews Count': '0.0',
        'Star Reviews': '0',
        'Date Gathered': '2024-05-08',
        'Date Gathered Hours': '2024-05-08 08:27:29'
    }
]

overall_impressions = [
    (
        'December, 2023',
        '0 impressions',
        '1,874 impressions',
        'https://app.rankbreeze.com/rankings/71585',
        '71585',
        'Windsor Island Resort 5br Villa Pool near Disney',
        '2024-05-08',
        '2024-05-08 08:27:29'
    ),
    (
        'January, 2024',
        '0 impressions',
        '2,365 impressions',
        'https://app.rankbreeze.com/rankings/71585',
        '71585',
        'Windsor Island Resort 5br Villa Pool near Disney',
        '2024-05-08',
        '2024-05-08 08:27:29'
    )
]

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
