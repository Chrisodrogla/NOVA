import json
import csv
import sys
sys.path.insert(0, "C:\\Users\\calgo\\Github_vscode_Cloned\\NOVA\\scraper")
import concurrent.futures
from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy
import logging




rental_links = [

    {
        "listing_link_format": "https://www.airbnb.com/s/Kissimmee--Florida--United-States/homes?tab_id=home_tab&refinement_paths[]=/homes&flexible_trip_lengths[]=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&source=structured_search_input_header&search_type=autocomplete_click&query=Kissimmee,%20Florida,%20United%20States&price_filter_num_nights=4&rank_mode=default&date_picker_type=calendar&checkin=2024-05-26&checkout=2024-05-26&min_bedrooms=6&min_beds=8&min_bathrooms=10&adults=14&currency=USD",
        "rankbreeze_Id": "69715",
        "rental_id": "37938829"
    },
    {
        "listing_link_format": "https://www.airbnb.com/s/Kissimmee--Florida--United-States/homes?tab_id=home_tab&refinement_paths[]=/homes&flexible_trip_lengths[]=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&source=structured_search_input_header&search_type=autocomplete_click&query=Kissimmee,%20Florida,%20United%20States&price_filter_num_nights=4&rank_mode=default&date_picker_type=calendar&checkin=2024-05-26&checkout=2024-05-26&min_bedrooms=10&min_beds=16&min_bathrooms=10&adults=14&currency=USD",
        "rankbreeze_Id": "1212312369715",
        "rental_id": "21312312337938829"
    }
]


def filter_results(result, needed_keys):
    filtered_results = []
    for listing in result:
        for item in listing:
            filtered_result = {key: item.get(key, None) for key in needed_keys}
            filtered_results.append(filtered_result)
    return filtered_results


def scrape_rental(rental, scraper, needed_keys):
    config = {"url": rental["listing_link_format"]}
    result = scraper.execute(config)
    filtered_results = filter_results(result, needed_keys)
    final_results = []
    for filtered_result in filtered_results:
        final_result = {
            "rankbreeze_Id": rental["rankbreeze_Id"],
            "rental_id": rental["rental_id"],
            **filtered_result
        }
        final_results.append(final_result)
    return final_results


logger = logging.getLogger(__name__)
scraper = AirbnbComSearchStrategy(logger)
needed_keys = ['orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night', 'check_in_date',
               'check_out_date']


final_results = []


with concurrent.futures.ThreadPoolExecutor() as executor:

    futures = [executor.submit(scrape_rental, rental, scraper, needed_keys) for rental in rental_links]


    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            final_results.extend(result)
        except Exception as e:
            logger.error(f"Error occurred: {e}")


with open('C:\\Users\\calgo\\Github_vscode_Cloned\\NOVA\\scraper\\scraper\\Listing_Url\\final_rental_link.json', 'w') as f:
    json.dump(final_results, f, indent=4)


csv_columns = ['rankbreeze_Id', 'rental_id'] + needed_keys
with open('C:\\Users\\calgo\\Github_vscode_Cloned\\NOVA\\scraper\\scraper\\Listing_Url\\final_results.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in final_results:
        writer.writerow(data)



print("Done Running")        
print(final_results)      