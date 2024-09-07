import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
import logging
import os
from headers import HEADERS

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("scraper")

class AsyncScraper:
    def __init__(self, base_url, template, urls, start_page=1, page_param=None):
        logger.debug("Initializing AsyncScraper")
        self.base_url = base_url
        self.template = template
        self.urls = urls
        self.start_page = start_page
        self.page_param = page_param
        self.headers = HEADERS
        self.all_product_data = []

    async def fetch(self, session, url, params=None):
        try:
            logger.debug(f"Fetching URL: {url} with params: {params}")
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status != 200:
                    logger.error(f"Error fetching {url}: Status {response.status}")
                    return None
                text = await response.text()
                logger.info(f"Fetched {len(text)} characters from {url}")
                return text
        except Exception as e:
            logger.error(f"Exception while fetching {url}: {e}")
            return None

    async def scrape_url(self, url):
        logger.info(f"Scraping URL: {url}")

        async with aiohttp.ClientSession() as session:
            if self.page_param is None:
                # Single page scrape
                text = await self.fetch(session, url)
                if text is None:
                    return

                soup = BeautifulSoup(text, 'html.parser')
                if soup.title and soup.title.string.strip().lower() == "server error":
                    logger.error("Server error detected, stopping scrape.")
                    return

                products = self.extract_product_data(soup)
                if products:
                    self.all_product_data.extend(products)
                    logger.info(f"Scraped {len(products)} products from {url}")
            else:
                # Multi-page scrape
                current_page = self.start_page
                while True:
                    params = {self.page_param: current_page} if self.page_param else None
                    logger.info(f"Requesting URL: {url} with params: {params}")
                    text = await self.fetch(session, url, params=params)
                    if text is None:
                        break

                    soup = BeautifulSoup(text, 'html.parser')
                    if soup.title and soup.title.string.strip().lower() == "server error":
                        logger.error("Server error detected, stopping scrape.")
                        break

                    products = self.extract_product_data(soup)
                    if not products:
                        logger.info(f"No products found on page {current_page} of {url}, stopping scrape.")
                        break

                    self.all_product_data.extend(products)
                    logger.info(f"Scraped {len(products)} products from page {current_page} of {url}")

                    current_page += 1

    def extract_product_data(self, soup):
        product_data = []
        try:
            product_cards = soup.select(self.template["product_card_selector"])
            logger.info(f"Found {len(product_cards)} product cards")
            for card in product_cards:
                product_info = {}
                for field, selector in self.template["fields"].items():
                    element = card.select_one(selector)
                    if field == "Image":
                        product_info[field] = element["src"] if element else ''
                    elif field == "URL":
                        product_info[field] = element["href"] if element else ''
                    else:
                        product_info[field] = element.text.strip() if element else ''
                product_data.append(product_info)
            logger.info(f"Extracted {len(product_data)} products")
        except Exception as e:
            logger.error(f"Error extracting product data: {e}")
        return product_data

    async def scrape_all(self):
        if len(self.urls) == 1 and self.page_param is None:
            # Single URL, no params, no concurrency
            await self.scrape_url(self.urls[0])
        else:
            # Multiple URLs or params are present, use concurrency
            tasks = [self.scrape_url(url) for url in self.urls]
            await asyncio.gather(*tasks)

    def run_async(self):
        logger.debug("Running async scraping")
        asyncio.run(self.scrape_all())

    def save_to_csv(self, filename=None):
        try:
            if filename is None:
                filename = f"{self.base_url.replace('https://', '').replace('http://', '').replace('/', '_')}_products.csv"
            data_directory = "data"
            if not os.path.exists(data_directory):
                os.makedirs(data_directory)
            filepath = os.path.join(data_directory, filename)
            logger.info(f"Saving data to {filepath}")
            df = pd.DataFrame(self.all_product_data)
            df.to_csv(filepath, index=False, sep=";", encoding="utf-8-sig")
            logger.info(f"Data saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving data to CSV: {e}")
