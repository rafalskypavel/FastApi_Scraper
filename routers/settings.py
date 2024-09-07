import json
import os
import logging
from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

SETTINGS_FILE = "scraping_settings.json"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def settings(request: Request):
    settings_data = load_settings()
    return templates.TemplateResponse("settings.html", {"request": request, "settings": settings_data})

def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as file:
                settings = json.load(file)
                # logger.info(f"Loaded settings: {json.dumps(settings, ensure_ascii=False, indent=4)}")
                return settings
    except Exception as e:
        logger.error(f"Error loading settings: {e}")
    return {}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as file:
            # Convert the field types back to a simple dictionary before saving
            for base_url, details in settings.items():
                for field, value in details['template']['fields'].items():
                    if isinstance(value, dict) and 'selector' in value and 'type' in value:
                        details['template']['fields'][field] = value
            json.dump(settings, file, ensure_ascii=False, indent=4)
            # logger.info(f"Saved settings: {json.dumps(settings, ensure_ascii=False, indent=4)}")
    except Exception as e:
        logger.error(f"Error saving settings: {e}")
