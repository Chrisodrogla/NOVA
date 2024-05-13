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
    "https://app.rankbreeze.com/rankings/71571",
    "https://app.rankbreeze.com/rankings/71570",
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
    "https://app.rankbreeze.com/rankings/70455",
    "https://app.rankbreeze.com/rankings/70454",
    "https://app.rankbreeze.com/rankings/70453",
    "https://app.rankbreeze.com/rankings/70452",
    "https://app.rankbreeze.com/rankings/70451",
    "https://app.rankbreeze.com/rankings/70450",
    "https://app.rankbreeze.com/rankings/70449",
    "https://app.rankbreeze.com/rankings/70448",
    "https://app.rankbreeze.com/rankings/70173",
    "https://app.rankbreeze.com/rankings/70165",
    "https://app.rankbreeze.com/rankings/69727",
    "https://app.rankbreeze.com/rankings/69725",
    "https://app.rankbreeze.com/rankings/69724",
    "https://app.rankbreeze.com/rankings/69723",
    "https://app.rankbreeze.com/rankings/69722",
    "https://app.rankbreeze.com/rankings/69721",
    "https://app.rankbreeze.com/rankings/69720",
    "https://app.rankbreeze.com/rankings/69719",
    "https://app.rankbreeze.com/rankings/69718",
    "https://app.rankbreeze.com/rankings/69717",
    "https://app.rankbreeze.com/rankings/69716",
    "https://app.rankbreeze.com/rankings/69715",
    "https://app.rankbreeze.com/rankings/69713",
    "https://app.rankbreeze.com/rankings/69712",
    "https://app.rankbreeze.com/rankings/69711",
    "https://app.rankbreeze.com/rankings/69709",
    "https://app.rankbreeze.com/rankings/69708",
    "https://app.rankbreeze.com/rankings/69139",
    "https://app.rankbreeze.com/rankings/69138",
    "https://app.rankbreeze.com/rankings/69136",
    "https://app.rankbreeze.com/rankings/69006",
    "https://app.rankbreeze.com/rankings/69005",
    "https://app.rankbreeze.com/rankings/69004",
    "https://app.rankbreeze.com/rankings/68864",
    "https://app.rankbreeze.com/rankings/68473",
    "https://app.rankbreeze.com/rankings/68472",
    "https://app.rankbreeze.com/rankings/67938",
    "https://app.rankbreeze.com/rankings/67937",
    "https://app.rankbreeze.com/rankings/67936",
    "https://app.rankbreeze.com/rankings/67935",
    "https://app.rankbreeze.com/rankings/67713",
    "https://app.rankbreeze.com/rankings/67712",
    "https://app.rankbreeze.com/rankings/67710",
    "https://app.rankbreeze.com/rankings/67709",
    "https://app.rankbreeze.com/rankings/67708",
    "https://app.rankbreeze.com/rankings/67707",
    "https://app.rankbreeze.com/rankings/67706",
    "https://app.rankbreeze.com/rankings/67705",
    "https://app.rankbreeze.com/rankings/67704",
    "https://app.rankbreeze.com/rankings/67702",
    "https://app.rankbreeze.com/rankings/67701",
    "https://app.rankbreeze.com/rankings/67700",
    "https://app.rankbreeze.com/rankings/67699",
    "https://app.rankbreeze.com/rankings/67698",
    "https://app.rankbreeze.com/rankings/67696",
    "https://app.rankbreeze.com/rankings/67693",
    "https://app.rankbreeze.com/rankings/67692",
    "https://app.rankbreeze.com/rankings/67691",
    "https://app.rankbreeze.com/rankings/67690",
    "https://app.rankbreeze.com/rankings/67689",
    "https://app.rankbreeze.com/rankings/67688",
    "https://app.rankbreeze.com/rankings/67686",
    "https://app.rankbreeze.com/rankings/67685",
    "https://app.rankbreeze.com/rankings/67684",
    "https://app.rankbreeze.com/rankings/67683",
    "https://app.rankbreeze.com/rankings/67682",
    "https://app.rankbreeze.com/rankings/67681",
    "https://app.rankbreeze.com/rankings/67678",
    "https://app.rankbreeze.com/rankings/67677",
    "https://app.rankbreeze.com/rankings/67676",
    "https://app.rankbreeze.com/rankings/67675",
    "https://app.rankbreeze.com/rankings/67673",
    "https://app.rankbreeze.com/rankings/67646",
    "https://app.rankbreeze.com/rankings/67645",
    "https://app.rankbreeze.com/rankings/67643",
    "https://app.rankbreeze.com/rankings/67642",
    "https://app.rankbreeze.com/rankings/67641",
    "https://app.rankbreeze.com/rankings/67640",
    "https://app.rankbreeze.com/rankings/67638",
    "https://app.rankbreeze.com/rankings/67565",
    "https://app.rankbreeze.com/rankings/67564",
    "https://app.rankbreeze.com/rankings/67562",
    "https://app.rankbreeze.com/rankings/67561",
    "https://app.rankbreeze.com/rankings/67556",
    "https://app.rankbreeze.com/rankings/67555",
    "https://app.rankbreeze.com/rankings/67548",
    "https://app.rankbreeze.com/rankings/67447",
    "https://app.rankbreeze.com/rankings/67446",
    "https://app.rankbreeze.com/rankings/67445",
    "https://app.rankbreeze.com/rankings/67444",
    "https://app.rankbreeze.com/rankings/67443",
    "https://app.rankbreeze.com/rankings/67442",
    "https://app.rankbreeze.com/rankings/67441",
    "https://app.rankbreeze.com/rankings/67439",
    "https://app.rankbreeze.com/rankings/67438",
    "https://app.rankbreeze.com/rankings/67434",
    "https://app.rankbreeze.com/rankings/67433",
    "https://app.rankbreeze.com/rankings/67432",
    "https://app.rankbreeze.com/rankings/67425",
    "https://app.rankbreeze.com/rankings/67421",
    "https://app.rankbreeze.com/rankings/67420",
    "https://app.rankbreeze.com/rankings/67419",
    "https://app.rankbreeze.com/rankings/67417",
    "https://app.rankbreeze.com/rankings/67416",
    "https://app.rankbreeze.com/rankings/67415",
    "https://app.rankbreeze.com/rankings/67414",
    "https://app.rankbreeze.com/rankings/67266",
    "https://app.rankbreeze.com/rankings/67265",
    "https://app.rankbreeze.com/rankings/67117",
    "https://app.rankbreeze.com/rankings/66980",
    "https://app.rankbreeze.com/rankings/66966",
    "https://app.rankbreeze.com/rankings/66768",
    "https://app.rankbreeze.com/rankings/66766",
    "https://app.rankbreeze.com/rankings/66765",
    "https://app.rankbreeze.com/rankings/66764",
    "https://app.rankbreeze.com/rankings/66763",
    "https://app.rankbreeze.com/rankings/66761",
    "https://app.rankbreeze.com/rankings/66760",
    "https://app.rankbreeze.com/rankings/66758",
    "https://app.rankbreeze.com/rankings/66755",
    "https://app.rankbreeze.com/rankings/66752",
    "https://app.rankbreeze.com/rankings/66751",
    "https://app.rankbreeze.com/rankings/66750",
    "https://app.rankbreeze.com/rankings/66747",
    "https://app.rankbreeze.com/rankings/66739",
    "https://app.rankbreeze.com/rankings/66738",
    "https://app.rankbreeze.com/rankings/66734",
    "https://app.rankbreeze.com/rankings/66733",
    "https://app.rankbreeze.com/rankings/66732",
    "https://app.rankbreeze.com/rankings/66731",
    "https://app.rankbreeze.com/rankings/66729",
    "https://app.rankbreeze.com/rankings/66728",
    "https://app.rankbreeze.com/rankings/66721",
    "https://app.rankbreeze.com/rankings/66720",
    "https://app.rankbreeze.com/rankings/66718",
    "https://app.rankbreeze.com/rankings/66717",
    "https://app.rankbreeze.com/rankings/66716",
    "https://app.rankbreeze.com/rankings/66715",
    "https://app.rankbreeze.com/rankings/66686",
    "https://app.rankbreeze.com/rankings/66685",
    "https://app.rankbreeze.com/rankings/66684",
    "https://app.rankbreeze.com/rankings/66271",
    "https://app.rankbreeze.com/rankings/66263",
    "https://app.rankbreeze.com/rankings/66262",
    "https://app.rankbreeze.com/rankings/64860",
    "https://app.rankbreeze.com/rankings/64853",
    "https://app.rankbreeze.com/rankings/64827",
    "https://app.rankbreeze.com/rankings/64810",
    "https://app.rankbreeze.com/rankings/59394",
    "https://app.rankbreeze.com/rankings/59090",
    "https://app.rankbreeze.com/rankings/58925",
    "https://app.rankbreeze.com/rankings/58918",
    "https://app.rankbreeze.com/rankings/58911",
    "https://app.rankbreeze.com/rankings/58908",
    "https://app.rankbreeze.com/rankings/58012",
    "https://app.rankbreeze.com/rankings/57739",
    "https://app.rankbreeze.com/rankings/56233",
    "https://app.rankbreeze.com/rankings/56225",
    "https://app.rankbreeze.com/rankings/55145",
    "https://app.rankbreeze.com/rankings/54372",
    "https://app.rankbreeze.com/rankings/53629",
    "https://app.rankbreeze.com/rankings/53102",
    "https://app.rankbreeze.com/rankings/53081",
    "https://app.rankbreeze.com/rankings/52672",
    "https://app.rankbreeze.com/rankings/52636",
    "https://app.rankbreeze.com/rankings/52634",
    "https://app.rankbreeze.com/rankings/52485",
    "https://app.rankbreeze.com/rankings/52484",
    "https://app.rankbreeze.com/rankings/52474",
    "https://app.rankbreeze.com/rankings/51110",
    "https://app.rankbreeze.com/rankings/51105",
    "https://app.rankbreeze.com/rankings/51100",
    "https://app.rankbreeze.com/rankings/51099",
    "https://app.rankbreeze.com/rankings/51096",
    "https://app.rankbreeze.com/rankings/51087",
    "https://app.rankbreeze.com/rankings/51078",
    "https://app.rankbreeze.com/rankings/51077",
    "https://app.rankbreeze.com/rankings/51074",
    "https://app.rankbreeze.com/rankings/51045",
    "https://app.rankbreeze.com/rankings/51022",
    "https://app.rankbreeze.com/rankings/50571",
    "https://app.rankbreeze.com/rankings/50329",
    "https://app.rankbreeze.com/rankings/50327",
    "https://app.rankbreeze.com/rankings/50320",
    "https://app.rankbreeze.com/rankings/50318",
    "https://app.rankbreeze.com/rankings/50312",
    "https://app.rankbreeze.com/rankings/50307",
    "https://app.rankbreeze.com/rankings/50254",
    "https://app.rankbreeze.com/rankings/50117" ]

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

# driver.quit()



overall_impressions = [(item[0], item[1].replace("impressions", "").replace(",","").strip(), item[2].replace("impressions", "").replace(",", "").strip(), *item[3:]) for item in overall_impressions]

overall_click_throughs = [(item[0], item[1].replace("%", "").strip(), item[2].replace("%", "").strip(), *item[3:]) for item in overall_conversion_rate]

overall_listing_views = [(item[0], item[1].replace("views", "").replace(",","").strip(), item[2].replace("views", "").replace(",","").strip(), *item[3:]) for item in overall_listing_views]

overall_conversion_rate = [(item[0], item[1].replace("%", "").strip(), item[2].replace("%", "").strip(), *item[3:]) for item in overall_conversion_rate]

overall_lead_times = [(item[0], item[1].replace("days", "").replace(",","").strip(), item[2].replace("days", "").replace(",","").strip(), *item[3:]) for item in overall_lead_times]

overall_airbnb_occupancy = [(item[0], item[1].replace("%", "").replace(",","").strip(), item[2].replace("%", "").replace(",","").strip(), *item[3:]) for item in overall_airbnb_occupancy]

overall_avg_daily_rates = [(item[0], item[1].replace("$", "").replace(",","").strip(), item[2].replace("$", "").replace(",","").strip(), *item[3:]) for item in  overall_avg_daily_rates]

overall_revenue = [(item[0], item[1].replace("$", "").replace(",","").strip(), *item[2:]) for item in overall_revenue] 

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
