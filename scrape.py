import requests
from datetime import datetime
from bs4 import BeautifulSoup as BS
from format_date2 import get_datetime2
from pathlib import Path
import json
import argparse
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

load_dotenv()

def get_listing_details(listing_url):
    res = requests.get(listing_url)
    detail = BS(res.text, 'html.parser')
    detail = detail.find('div', {'itemprop': 'description'}).get_text()
    detail = ' '.join(detail.split()).lstrip('Lisätiedot ')
    return detail

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
        response = requests.get(URL)

        page = BS(response.text, "html.parser")
        listings = page.find_all('a', class_='item_row_flex')


        for i,listing in enumerate(listings, start=1):
            id = listing.get('id')
            title = listing.find('div', class_="li-title").contents[0]
            try:
                price = int(listing.find('p', class_="list_price").contents[0].replace(" ", "").replace("€", ""))
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
            detail_uri = listing.get('href')
            description = get_listing_details(detail_uri)

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
                    "time_stamp": date,
                    "description": description
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
        logging.info(f'page number: {URL_page_no} - listings:{len(product_listing)}')

    timef = '%d.%m.%Y %H:%M'
    pmap = map(
        lambda b: {**b, 'time_stamp': b['time_stamp'].strftime(timef)}, product_listing)
    product_listing_json = json.dumps(list(pmap))

    return product_listing_json, product_listing

def run(region, category, subcategory, query, timeback, dest):
    d = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    logging.info("2")
    #try:
    prod_list_json, prod_list = get_listing_items(
        region=region,
        cat=category,
        subcat=subcategory,
        query=query if query else "",
        timeback=timeback)
    #except Exception:
    #    logging.info(Exception)
    #    raise IOError('Could not get items')

    if dest == 'local':
        Path('./out').mkdir(exist_ok=True)
        with open(f'./out/out_{d}.json', 'w') as f:
            parsed_json = json.loads(prod_list_json)
            f.write(json.dumps(parsed_json, indent=4, sort_keys=True))

    elif dest == 'mongo':
        uri = os.getenv("MONGODB_URI")
        client = MongoClient(uri)
        db = client['tavaralle-hinta']
        db.listings.insert_many(prod_list)
        db.insertOps.insert_one({'created': datetime.now(), 'insert_count': len(prod_list)})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', dest='region',
                        help='Region to search from, e.g. koko_suomi, uusimaa, varsinais-suomi')
    parser.add_argument('--category', dest='category',
                        help='Top-level listing category, e.g. puhelimet_ja_tarvikkeet')
    parser.add_argument('--subcategory', dest='subcategory',
                        help='Listing subcategory, e.g. puhelimet')
    parser.add_argument('--query', dest='query',
                        help='Additional search string for filtering results, e.g. Samsung, iPhone')
    parser.add_argument('--timeback', dest='timeback', type=int,
                        help='Time in days counting back from current time to include in search')
    parser.add_argument('--dest', dest='dest',
                        help='Choose either "mongo" to write results to database or "local" to write to file',
                        default='local')
    args = parser.parse_args()

    run(region=args.region,
        category=args.category,
        subcategory=args.subcategory,
        query=args.query,
        timeback=args.timeback,
        dest=args.dest)
    
        


    