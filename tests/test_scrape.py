import unittest
import responses
import requests
import json

from datetime import datetime as dt
from scrape import get_listing_details, handle_listing_page
from pathlib import Path
from bs4 import BeautifulSoup as BS

class TestScrapeFunctions(unittest.TestCase):

    @responses.activate
    def test_get_listing_details(self):
        mock_detail = Path('../data/test_detail_page.html').read_text()
        expect = 'Huippu 12gb RAM muistilla ja 256gb tallennustilalla varustettuna. Väriltään sininen. Puhelin on viime kesänä ostettu ja mukaan tulee laturi, sekä alkuperäispakkaus. Puhelimessa ei ole halkeamia tms. vaan sitä on pidetty hyvänä. Nouto Helsingistä tai ostajalle postikulut.'
        responses.add(responses.GET, 
                      'http://mock_detail_uri',
                      status=200,
                      body=mock_detail)
        detail = get_listing_details('http://mock_detail_uri')
        self.assertEqual(expect, detail)

    def test_get_list_view(self):
        mock_list = Path('../data/test_list_to_detail.html').read_text()
        mock_list = BS(mock_list, 'html.parser')
        expect = json.loads(Path('../data/expect_list.json').read_text())
        listings = handle_listing_page(mock_list,
                                       region='lappi',
                                       cat='puhelimet_ja_tarvikkeet',
                                       subcat='puhelimet',
                                       timeback=3)
        timef = '%d.%m.%Y %H:%M'
        listings = list(map(
            lambda b: {**b, 'time_stamp': b['time_stamp'].strftime(timef), 'image_link': None}, listings))
        expect = list(map(
            lambda b: {**b, 'image_link': None}, expect))
        self.assertDictEqual(expect[0], listings[0])
        self.assertEqual(expect, listings)

if __name__ == '__main__':
    unittest.main()
