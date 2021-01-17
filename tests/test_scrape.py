import unittest
import responses
import requests

from scrape import get_listing_details
from pathlib import Path

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

if __name__ == '__main__':
    unittest.main()
