from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import json

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Placeholder function to fetch real data
def fetch_real_dashboard_data():
    try:
        with open("./scraping_settings.json", "r", encoding="utf-8") as f:
            scraping_data = json.load(f)

        total_suppliers = len(scraping_data)
        successful_scrapes = sum(1 for supplier in scraping_data.values() if "success" in supplier)
        scrape_errors = sum(1 for supplier in scraping_data.values() if "error" in supplier)
        recent_scrapes = [
            {"supplier_name": "Garwin", "status": "Success", "date": "2024-07-27"},
            {"supplier_name": "For-est", "status": "Error", "date": "2024-07-26"},
            {"supplier_name": "Garwin", "status": "Success", "date": "2024-07-25"},
        ]
        popular_suppliers = [
            {"name": "Garwin", "usage_count": 15},
            {"name": "For-est", "usage_count": 10},
        ]

        return {
            "total_suppliers": total_suppliers,
            "successful_scrapes": successful_scrapes,
            "scrape_errors": scrape_errors,
            "recent_scrapes": recent_scrapes,
            "popular_suppliers": popular_suppliers
        }
    except Exception as e:
        print(f"Error fetching dashboard data: {e}")
        return {
            "total_suppliers": 0,
            "successful_scrapes": 0,
            "scrape_errors": 0,
            "recent_scrapes": [],
            "popular_suppliers": []
        }


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    dashboard_data = fetch_real_dashboard_data()
    return templates.TemplateResponse("dashboard.html", {"request": request, **dashboard_data})
