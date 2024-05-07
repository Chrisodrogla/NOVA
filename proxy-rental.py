import os
import time
import datetime
from selenium import webdriver
import shutil
import json
from selenium.common.exceptions import NoSuchElementException

username = os.environ['D_USERNAME_SECRET']
passw = os.environ['D_PASSWORD_SECRET']

website = "https://app.rankbreeze.com/listings"

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(options=options)
driver.get(website)

time.sleep(2)

driver.find_element("xpath", """(//div[@class="form-group"]/input)[1]""").send_keys(username)
time.sleep(2)
driver.find_element("xpath", """(//div[@class="form-group"]/input)[2]""").send_keys(passw)
log = driver.find_element("xpath", """(//div[@class="form-group"]/input)[3]""")
time.sleep(2)
log.click()
time.sleep(20)

proxy_links = []

while True:
    # Get all the desired links on the current page
    links = driver.find_elements("xpath", """//a[@class="btn btn-outline-primary card-btn custom-nav-button mr-1"]""")
    for link in links:
        web = link.get_attribute("href")
        proxy_links.append(web)

    time.sleep(10)
    # Check if there's a "Next" button on the page
    next_buttons = driver.find_elements("xpath", """//span[@class="next"]""")
    if len(next_buttons) > 0:
        # Click the first "Next" button
        next_buttons[0].click()
    else:
        # No "Next" button, exit the loop
        break

#############################################
driver.quit()
# Name of the JSON file
json_filename = "proxy-rental-link.json"

# Step 1: Read existing links from the JSON file if it exists
if os.path.exists(json_filename):
    with open(json_filename, "r") as json_file:
        existing_links = json.load(json_file)
else:
    existing_links = []  # If the file doesn't exist, start with an empty list

# Step 3: Only add unique links to existing_links
for link in proxy_links:
    if link not in existing_links:
        existing_links.append(link)  # Add the link if it's not already in the list

# Step 4: Write the updated list back to the JSON file
with open(json_filename, "w") as json_file:
    json.dump(existing_links, json_file, indent=4)  # 'indent=4' for pretty-printing

