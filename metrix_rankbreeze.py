import os
import pyodbc
import time
from selenium import webdriver
import shutil
from selenium.common.exceptions import NoSuchElementException
import datetime
import pytz
import pandas as pd
import json






eastern_tz = pytz.timezone("America/New_York")
current_time = datetime.datetime.now(eastern_tz)

username = os.environ['D_USERNAME_SECRET']
passw = os.environ['D_PASSWORD_SECRET']

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
time.sleep(3)  # 20

proxy_links = ["https://app.rankbreeze.com/rankings/71585",
#     "https://app.rankbreeze.com/rankings/71572",
    "https://app.rankbreeze.com/rankings/71571",
    "https://app.rankbreeze.com/rankings/71570",
#     "https://app.rankbreeze.com/rankings/71569",
    "https://app.rankbreeze.com/rankings/71568",
    "https://app.rankbreeze.com/rankings/71567",
    "https://app.rankbreeze.com/rankings/71363",
    "https://app.rankbreeze.com/rankings/71362",
    "https://app.rankbreeze.com/rankings/71361",
    "https://app.rankbreeze.com/rankings/71360",
    "https://app.rankbreeze.com/rankings/71359",
    "https://app.rankbreeze.com/rankings/71358",
    "https://app.rankbreeze.com/rankings/70897",
    "https://app.rankbreeze.com/rankings/70895",
    "https://app.rankbreeze.com/rankings/70894",
    "https://app.rankbreeze.com/rankings/70893",
    "https://app.rankbreeze.com/rankings/70892",
    "https://app.rankbreeze.com/rankings/70891",
    "https://app.rankbreeze.com/rankings/70890",
    "https://app.rankbreeze.com/rankings/70889",
    "https://app.rankbreeze.com/rankings/70888",
    "https://app.rankbreeze.com/rankings/70887",
    "https://app.rankbreeze.com/rankings/70886",
    "https://app.rankbreeze.com/rankings/70885",
    "https://app.rankbreeze.com/rankings/70884",
    "https://app.rankbreeze.com/rankings/70883",
    "https://app.rankbreeze.com/rankings/70882",
    "https://app.rankbreeze.com/rankings/70881",
    "https://app.rankbreeze.com/rankings/70862",
    "https://app.rankbreeze.com/rankings/70861",
    "https://app.rankbreeze.com/rankings/70860",
    "https://app.rankbreeze.com/rankings/70859",
    "https://app.rankbreeze.com/rankings/70858",
    "https://app.rankbreeze.com/rankings/70852",
    "https://app.rankbreeze.com/rankings/70851",
    "https://app.rankbreeze.com/rankings/70515",
    "https://app.rankbreeze.com/rankings/70479",
    "https://app.rankbreeze.com/rankings/70476",
    "https://app.rankbreeze.com/rankings/70475",
    "https://app.rankbreeze.com/rankings/70474",
    "https://app.rankbreeze.com/rankings/70473",
    "https://app.rankbreeze.com/rankings/70472",
    "https://app.rankbreeze.com/rankings/70471",
    "https://app.rankbreeze.com/rankings/70470",
    "https://app.rankbreeze.com/rankings/70468",
    "https://app.rankbreeze.com/rankings/70467",
    "https://app.rankbreeze.com/rankings/70466",
    "https://app.rankbreeze.com/rankings/70465",
    "https://app.rankbreeze.com/rankings/70464",
    "https://app.rankbreeze.com/rankings/70463",
    "https://app.rankbreeze.com/rankings/70462",
    "https://app.rankbreeze.com/rankings/70461",
    "https://app.rankbreeze.com/rankings/70460",
    "https://app.rankbreeze.com/rankings/70459",
    "https://app.rankbreeze.com/rankings/70458",
    "https://app.rankbreeze.com/rankings/70457",
    "https://app.rankbreeze.com/rankings/70456",
    "https://app.rankbreeze.com/rankings/70455", ]

data = []
overall_impressions = []
overall_click_throughs = []
overall_listing_views = []
overall_conversion_rate = []
overall_lead_times = []
overall_airbnb_occupancy = []
overall_avg_daily_rates = []
overall_revenue = []

for website in proxy_links:
    driver.get(website)
    time.sleep(2)

    driver.get(website)

    time.sleep(2)

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
    overall_click_throughs.extend(extract_table_data(search_conversion_rate, 3))
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

driver.quit()

def clean_data(data_list, *replace_chars):
    return [(item[0], *(value.replace(*replace_chars).replace(",", "").strip() for value in item[1:])) for item in data_list]

overall_impressions = clean_data(overall_impressions, "impressions")
overall_click_throughs = clean_data(overall_click_throughs, "%")
overall_listing_views = clean_data(overall_listing_views, "views")
overall_conversion_rate = clean_data(overall_conversion_rate, "%")
overall_lead_times = clean_data(overall_lead_times, "days")
overall_airbnb_occupancy = clean_data(overall_airbnb_occupancy, "%")
overall_avg_daily_rates = clean_data(overall_avg_daily_rates, "$")
overall_revenue = [(item[0], *(value.replace("$", "").replace(",", "").strip() for value in item[1:])) for item in overall_revenue]

# overall_impressions = [(item[0], item[1].replace("impressions", "").replace(",","").strip(), item[2].replace("impressions", "").replace(",", "").strip(), *item[3:]) for item in overall_impressions]

# overall_click_throughs = [(item[0], item[1].replace("%", "").strip(), item[2].replace("%", "").strip(), *item[3:]) for item in overall_conversion_rate]

# overall_listing_views = [(item[0], item[1].replace("views", "").replace(",","").strip(), item[2].replace("views", "").replace(",","").strip(), *item[3:]) for item in overall_listing_views]

# overall_conversion_rate = [(item[0], item[1].replace("%", "").strip(), item[2].replace("%", "").strip(), *item[3:]) for item in overall_conversion_rate]

# overall_lead_times = [(item[0], item[1].replace("days", "").replace(",","").strip(), item[2].replace("days", "").replace(",","").strip(), *item[3:]) for item in overall_lead_times]

# overall_airbnb_occupancy = [(item[0], item[1].replace("%", "").replace(",","").strip(), item[2].replace("%", "").replace(",","").strip(), *item[3:]) for item in overall_airbnb_occupancy]

# overall_avg_daily_rates = [(item[0], item[1].replace("$", "").replace(",","").strip(), item[2].replace("$", "").replace(",","").strip(), *item[3:]) for item in  overall_avg_daily_rates]

# overall_revenue = [(item[0], item[1].replace("$", "").replace(",","").strip(), *item[2:]) for item in overall_revenue] 

connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')

# Establish connection
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Retrieve insert queries
# insert_query1 = os.environ.get("INSERT_QUERY_1")

# insert_query2 = os.environ.get("INSERT_QUERY_2")

# insert_query3 = os.environ.get("INSERT_QUERY_3")

# insert_query4 = os.environ.get("INSERT_QUERY_4")

# insert_query5 = os.environ.get("INSERT_QUERY_5")

# insert_query6 = os.environ.get("INSERT_QUERY_6")

# insert_query7 = os.environ.get("INSERT_QUERY_7")

# insert_query8 = os.environ.get("INSERT_QUERY_8")

# insert_query9 = os.environ.get("INSERT_QUERY_9")

insert_query1 = "INSERT INTO RankReview (link, link_id, rental_title, guest_satisfaction, review_count, date_data_gathered, time_data_gathered) VALUES (?, ?, ?, ?, ?, ?, ?)"

insert_query2 = "INSERT INTO RankImpression (period, impressions, similar_listing, link, link_id, rental_title, date_data_gathered, time_data_gathered) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

insert_query3 = "INSERT INTO RankClick (period, click_trough, similar_listing, link, link_id, rental_title, date_data_gathered, time_data_gathered) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

insert_query4 = "INSERT INTO RankListingView (period, listing_view, similar_listing, link, link_id, rental_title, date_data_gathered, time_data_gathered) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

insert_query5 = "INSERT INTO RankConversionRate (period, conversion, similar_listing, link, link_id, rental_title, date_data_gathered, time_data_gathered) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

insert_query6 = "INSERT INTO RankLeadTime (period, lead_time, similar_listing, link, link_id, rental_title, date_data_gathered, time_data_gathered) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

insert_query7 = "INSERT INTO RankAirbnbOccupancy (period, airbnb_occupancy, similar_listing, link, link_id, rental_title, date_data_gathered, time_data_gathered) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

insert_query8 = "INSERT INTO RankAvgDailyRate (period, avg_daily_rate, similar_listing, link, link_id, rental_title, date_data_gathered, time_data_gathered) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

insert_query9 = "INSERT INTO RankRevenue (period, revenue, link, link_id, rental_title, date_data_gathered, time_data_gathered) VALUES (?, ?, ?, ?, ?, ?, ?)"



# Insert data into table1
for item in data:
    cursor.execute(insert_query1, (item['Link'], item['Link Id'], item['Rental Name'], item['Star Reviews'], item['Reviews Count'], item['Date Gathered'], item['Date Gathered Hours']))

# Combine all data and queries into one list
data_and_queries = [
    (overall_impressions, insert_query2),
    (overall_click_throughs, insert_query3),
    (overall_listing_views, insert_query4),
    (overall_conversion_rate, insert_query5),
    (overall_lead_times, insert_query6),
    (overall_airbnb_occupancy, insert_query7),
    (overall_avg_daily_rates, insert_query8),
    (overall_revenue, insert_query9)
]

# Execute all queries in a single loop
for data, query in data_and_queries:
    for item in data:
        cursor.execute(query, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], *item[7:]))


# # Insert data into table2
# for item in overall_impressions:
#     cursor.execute(insert_query2, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

# for item in overall_click_throughs:
#     cursor.execute(insert_query3, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

# for item in overall_listing_views:
#     cursor.execute(insert_query4, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

# for item in overall_conversion_rate:
#     cursor.execute(insert_query5, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

# for item in overall_lead_times:
#     cursor.execute(insert_query6, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

# for item in overall_airbnb_occupancy:
#     cursor.execute(insert_query7, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

# for item in overall_avg_daily_rates:
#     cursor.execute(insert_query8, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

# for item in overall_revenue:
#     cursor.execute(insert_query9, (item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
print("Done Running to Workflow")

# # Commit changes
# conn.commit()

# # Close connection
# conn.close()
