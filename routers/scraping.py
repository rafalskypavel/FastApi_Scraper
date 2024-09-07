from fastapi import APIRouter, HTTPException
import urllib.parse
from scraper import AsyncScraper
from .settings import load_settings
import logging

logger = logging.getLogger("scraping")

router = APIRouter()
scraping_settings = load_settings()

@router.post("/start-scraping/{base_url:path}")
async def start_scraping(base_url: str, page_param: str = "None"):
    try:
        decoded_url = urllib.parse.unquote(base_url)
        if decoded_url not in scraping_settings:
            raise HTTPException(status_code=404, detail="URL not found.")

        settings = scraping_settings[decoded_url]
        template = settings["template"]

        # Обработка случая, если page_param равен None
        page_param = None if page_param == "None" else page_param

        scraper = AsyncScraper(
            decoded_url,
            template,
            settings["urls"],
            settings["start_page"],
            page_param
        )

        await scraper.scrape_all()
        scraper.save_to_csv(
            f"{decoded_url.replace('https://', '').replace('http://', '').replace('/', '_')}_products.csv")
        return {"message": f"Scraping completed for {decoded_url}"}
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
