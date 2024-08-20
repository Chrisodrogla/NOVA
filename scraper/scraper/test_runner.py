import time
import sys
sys.path.insert(0,"C:\\Users\\calgo\\Github_vscode_Cloned\\NOVA\\scraper")
from scraper.strategies.airbnb_com.search_page import AirbnbComDetailStrategy  #AirbnbComDetailStrategy
import logging

logger = logging.getLogger(__name__)

start_time = time.time()

scraper = AirbnbComDetailStrategy(logger)                  #AirbnbComDetailStrategy
config = {"url": "https://www.airbnb.com/rooms/607996043990435730"}
result = scraper.execute(config)


############################################################################################################################################################

needed_keys = ['guest', 'baths', 'beds', 'bedrooms']

# Create a new dictionary with only the needed keys
filtered_result = {key: result[key] for key in needed_keys}

# Print the filtered result
print(filtered_result)

############################################################################################################################################################
# needed_keys = ['orig_price_per_night','cleaning_fee', 'service_fee', 'total_price', 'price_per_night','total_price', 'check_in_date','check_out_date']
#
#
# filtered_results = []
#
#
# for listing in result:
#     for item in listing:
#         filtered_result = {key: item[key] for key in needed_keys}
#         filtered_results.append(filtered_result)
#
# print(filtered_results)
# print(len(filtered_results))
#
# # Record the end time
# end_time = time.time()
#
# # Calculate the elapsed time
# elapsed_time = end_time - start_time
# minutes = int(elapsed_time // 60)
# seconds = int(elapsed_time % 60)
#
# print(f"Time takes {minutes} minutes and {seconds} seconds")
