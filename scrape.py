import requests
from datetime import datetime
from bs4 import BeautifulSoup as BS
from format_date2 import get_datetime2
from pathlib import Path
import json
import argparse

def get_listing_items(region, cat, subcat, query, timeback):
    
    runtime = datetime.now()
    product_listing = []
    is_within_timeframe = True
    URL_page_no = 1
    listings_count = 0
    year_index = datetime.today().year
    days_of_year = [datetime.today().timetuple().tm_yday]

    while is_within_timeframe:

        URL = f'https://www.tori.fi/{region}/{cat}/{subcat}?q={query}&st=s&o=' + str(URL_page_no)
        print(URL)
        response = requests.get(URL)

        page = BS(response.text, "html.parser")
        listings = page.find_all('a', class_='item_row_flex')


        for i,listing in enumerate(listings, start=1):
            id = listing.get('id')
            title = listing.find('div', class_="li-title").contents[0]
            try:
                price = listing.find('p', class_="list_price").contents[0].replace(" ", "")
            except IndexError:
                price = "Ei ilmoitettu"
            try:
                _region = listing.find('div', class_="cat_geo").find('p').getText().replace(" ", "").replace("\n", "").replace("\t", "")
            except IndexError:
                _region = "Ei ilmoitettu"
            product_link = listing.get('href')
            try:
                image_link = listing.find('div', class_="item_image_div").img['src']
            except AttributeError:
                image_link = "Ei kuvaa"

            listing_date = listing.find('div', class_="date_image").contents[0]

            # Stopping condition #1 listing is older than specified timeframe
            date = get_datetime2(listing_date, year_index)
            tdiff = runtime - date
            if tdiff.days >= timeback:
                is_within_timeframe = False
                break
            else:
                item = {
                    "id": id,
                    "title": title,
                    "region": _region,
                    "category": cat,
                    "subcategory": subcat,
                    "price": price,
                    "product_link": product_link,
                    "image_link": image_link,
                    "time_stamp": date.strftime('%d.%m.%Y %H:%M')
                }

                doy = date.timetuple().tm_yday

                if not days_of_year[-1] == doy and any(doy >= d for d in days_of_year):
                    year_index = year_index - 1
                    days_of_year = []

                days_of_year.append(doy)
                product_listing.append(item)

        # Stopping condition #2 no more listings
        if len(product_listing) == listings_count:
            is_within_timeframe = False

        listings_count = len(product_listing)

        URL_page_no = URL_page_no + 1
        print(f'page number: {URL_page_no} - listings:{len(product_listing)}')

    product_listing_json = json.dumps(product_listing)

    return product_listing_json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', dest='region')
    parser.add_argument('--category', dest='category')
    parser.add_argument('--subcategory', dest='subcategory')
    parser.add_argument('--query', dest='query')
    parser.add_argument('--timeback', dest='timeback', type=int,
                        help='time in days counting back from current time to include in search')
    args = parser.parse_args()

    print(args.region)
    print(args.category)
    print(args.subcategory)
    print(args.query)
    print(args.timeback)
    
    d = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    Path('./out').mkdir(exist_ok=True)
    with open(f'./out/out_{d}.json', 'w') as f:
        try:
            prod_list = get_listing_items(
                region=args.region,
                cat=args.category,
                subcat=args.subcategory,
                query=args.query if args.query else "",
                timeback=args.timeback)

            parsed_json = json.loads(prod_list)
            f.write(json.dumps(parsed_json, indent=4, sort_keys=True))
        except:
            raise IOError('Could not get items')
    