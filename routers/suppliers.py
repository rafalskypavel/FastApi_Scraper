import json
import urllib.parse
import logging
from fastapi import APIRouter, HTTPException, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from .settings import load_settings, save_settings
from models import SupplierModel
from scraper import AsyncScraper

logger = logging.getLogger("suppliers")

router = APIRouter()
scraping_settings = load_settings()

templates = Jinja2Templates(directory="templates")


@router.get("/saved-suppliers", response_class=HTMLResponse)
def read_saved_suppliers(request: Request):
    return templates.TemplateResponse("saved_suppliers.html", {"request": request, "scraping_settings": scraping_settings})

@router.get("/add-supplier", response_class=HTMLResponse)
def read_add_supplier(request: Request):
    return templates.TemplateResponse("add_supplier.html", {"request": request})

@router.post("/add-supplier")
def add_supplier(supplier_model: SupplierModel):
    try:
        base_url = supplier_model.base_url
        if base_url in scraping_settings:
            raise HTTPException(status_code=400, detail="Supplier already exists.")
        scraping_settings[base_url] = {
            "start_page": supplier_model.start_page,
            "page_param": supplier_model.page_param,
            "template_name": supplier_model.template_name,
            "urls": supplier_model.urls,
            "template": {
                "product_card_selector": supplier_model.product_card_selector,
                "fields": supplier_model.fields
            }
        }
        save_settings(scraping_settings)
        logger.info(f"Supplier added: {base_url}")
        return {"message": "Supplier added successfully"}
    except Exception as e:
        logger.error(f"Error adding supplier: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/update-supplier/{base_url:path}")
def update_supplier(base_url: str, supplier_model: SupplierModel):
    try:
        decoded_url = urllib.parse.unquote(base_url)
        if decoded_url not in scraping_settings:
            raise HTTPException(status_code=404, detail="Supplier not found.")

        scraping_settings[decoded_url] = {
            "start_page": supplier_model.start_page,
            "page_param": supplier_model.page_param,
            "template_name": supplier_model.template_name,
            "urls": supplier_model.urls,
            "template": {
                "product_card_selector": supplier_model.product_card_selector,
                "fields": supplier_model.fields
            }
        }
        save_settings(scraping_settings)
        logger.info(f"Supplier updated: {decoded_url}")
        return {"message": "Supplier updated successfully"}
    except Exception as e:
        logger.error(f"Error updating supplier: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/delete-supplier/{base_url:path}")
def delete_supplier(base_url: str):
    try:
        logger.info(f"Received request to delete supplier: {base_url}")
        decoded_url = urllib.parse.unquote(base_url)
        logger.info(f"Decoded URL: {decoded_url}")
        logger.info(f"Current scraping settings: {json.dumps(scraping_settings, ensure_ascii=False, indent=4)}")
        if decoded_url not in scraping_settings:
            logger.error(f"Supplier not found in settings: {decoded_url}")
            raise HTTPException(status_code=404, detail="Supplier not found.")
        del scraping_settings[decoded_url]
        save_settings(scraping_settings)
        logger.info(f"Supplier deleted successfully: {decoded_url}")
        return {"message": "Supplier deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting supplier: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get-urls")
def get_urls():
    try:
        return scraping_settings
    except Exception as e:
        logger.error(f"Error getting URLs: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/test-supplier")
async def test_supplier(request: Request):
    try:
        data = await request.json()
        url = data['url']
        product_card_selector = data['product_card_selector']
        fields = data['fields']
        scraper = AsyncScraper(url, {"product_card_selector": product_card_selector, "fields": fields}, [url])
        await scraper.scrape_all()
        return {"result": scraper.all_product_data}
    except Exception as e:
        logger.error(f"Error testing supplier: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/start-scraping/{base_url:path}")
async def start_scraping(base_url: str):
    try:
        decoded_url = urllib.parse.unquote(base_url)
        if decoded_url not in scraping_settings:
            raise HTTPException(status_code=404, detail="URL not found.")
        settings = scraping_settings[decoded_url]
        template = settings["template"]
        scraper = AsyncScraper(decoded_url, template, settings["urls"], settings["start_page"], settings["page_param"])
        await scraper.scrape_all()
        scraper.save_to_csv(f"{decoded_url.replace('https://', '').replace('http://', '').replace('/', '_')}_products.csv")
        return {"message": f"Scraping completed for {decoded_url}"}
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
