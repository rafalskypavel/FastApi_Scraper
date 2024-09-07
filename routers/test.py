from fastapi import APIRouter, Request
from bs4 import BeautifulSoup
import aiohttp
import logging
from headers import HEADERS

logger = logging.getLogger("test")

router = APIRouter()

@router.post("/test-field")
async def test_field(request: Request):
    data = await request.json()
    url = data["url"]
    selector = data["selector"]
    type_ = data["type"]

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            if response.status != 200:
                return {"result": f"Error fetching {url}: Status {response.status}"}

            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            element = soup.select_one(selector)
            if element:
                value = element.text.strip()
                if type_ == "int":
                    value = int(value)
                elif type_ == "float":
                    value = float(value)
                return {"result": value}
            else:
                return {"result": f"No element found for selector {selector}"}

@router.post("/test-supplier")
async def test_supplier(request: Request):
    data = await request.json()
    url = data["url"]
    product_card_selector = data["product_card_selector"]
    fields = data["fields"]

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            if response.status != 200:
                return {"result": f"Error fetching {url}: Status {response.status}"}

            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            product_cards = soup.select(product_card_selector)
            if not product_cards:
                return {"result": f"No product cards found for selector {product_card_selector}"}

            product_data = []
            for card in product_cards:
                product_info = {}
                for field, details in fields.items():
                    element = card.select_one(details["selector"])
                    if element:
                        value = element.text.strip()
                        if details["type"] == "int":
                            value = int(value)
                        elif details["type"] == "float":
                            value = float(value)
                        product_info[field] = value
                    else:
                        product_info[field] = None
                product_data.append(product_info)

            return {"result": product_data}
