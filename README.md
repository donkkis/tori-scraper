### donkkis/tori-scraper

Just a simple parametrizable script to scrape listings from tori.fi, a finnish online flea market. Forked originally from https://github.com/W4SD/tori-scraper.

Upon each invokation of `scrape.py` results are written to `./out` directory as timestamped JSON files.

### Installation for local dev/test purposes

Recommended configuration is to use Python 3.8 together with `pip` and `virtualenv`

In project root, run:

1. `virtualenv .venv` or `virtualenv <path/to/python38/python .venv` if you need to set python executable explicitly
2. `.venv\Scripts\activate`
3. `pip install -r requirements.txt`

### Usage:

usage: scrape.py [-h] [--region REGION] [--category CATEGORY]
                 [--subcategory SUBCATEGORY] [--query QUERY]
                 [--timeback TIMEBACK]

optional arguments:
  -h, --help            show this help message and exit
  --region REGION       Region to search from, e.g. koko_suomi, uusimaa,
                        varsinais-suomi
  --category CATEGORY   Top-level listing category, e.g.
                        puhelimet_ja_tarvikkeet
  --subcategory SUBCATEGORY
                        Listing subcategory, e.g. puhelimet
  --query QUERY         Additional search string for filtering results, e.g.
                        Samsung, iPhone
  --timeback TIMEBACK   Time in days counting back from current time to
                        include in search

### Example

Get new listings from last 24 hours from whole Finland wherein `iPhone` appears a substring in listing title:

`python scrape.py --region koko_suomi --category puhelimet_ja_tarvikkeet --subcategory puhelimet --query iPhone --timeback 1`