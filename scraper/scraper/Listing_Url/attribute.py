import json
import sys
import logging


sys.path.insert(0, "C:\\Users\\calgo\\Downloads\\nova_scraper_\\scraper")


from scraper.strategies.airbnb_com.search_page import AirbnbComDetailStrategy


logger = logging.getLogger(__name__)

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def scrape_airbnb_details(data, scraper):
    updated_data = []
    needed_keys = ['guest', 'baths', 'beds', 'bedrooms']

    for item in data:
        config = {"url": item['airbnb_link']}
        result = scraper.execute(config)

        # Create a new dictionary with only the needed keys
        filtered_result = {key: result[key] for key in needed_keys}

        # Combine the original item with the filtered result
        combined_result = {**item, **filtered_result}
        updated_data.append(combined_result)

    return updated_data


def main():
    # File paths
    input_file = 'small_rb_bnb.json'
    output_file = 'listing_attribute.json'

    # Read the input JSON file
    data = read_json_file(input_file)

    # Initialize the scraper
    scraper = AirbnbComDetailStrategy(logger)

    # Scrape details for each Airbnb listing
    updated_data = scrape_airbnb_details(data, scraper)

    # Write the updated data to the output JSON file
    write_json_file(updated_data, output_file)

    print(f"Data has been successfully written to {output_file}")

if __name__ == "__main__":
    main()
