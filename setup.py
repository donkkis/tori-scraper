import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="donkkis", # Replace with your own username
    version="0.0.1",
    author="Panu Aho",
    author_email="panu.aho@gmail.com",
    description="Utility to scrape listings from tori.fi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donkkis/tori-scraper/",
    packages=setuptools.find_packages()
)
