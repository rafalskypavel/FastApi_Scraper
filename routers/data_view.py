import os
import csv
import logging
from fastapi import APIRouter, Request, HTTPException
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

DATA_DIRECTORY = "data"
logger = logging.getLogger(__name__)

@router.get("/", response_class=HTMLResponse)
def view_data(request: Request):
    return templates.TemplateResponse("data_view.html", {"request": request})

@router.get("/suppliers")
def get_suppliers():
    try:
        suppliers = [file.replace("_products.csv", "") for file in os.listdir(DATA_DIRECTORY) if file.endswith("_products.csv")]
        logger.info(f"Found suppliers: {suppliers}")
        return {"suppliers": suppliers}
    except Exception as e:
        logger.error(f"Error retrieving suppliers: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving suppliers: {e}")

@router.get("/supplier-data/{supplier_name}")
def get_supplier_data(supplier_name: str):
    file_path = os.path.join(DATA_DIRECTORY, f"{supplier_name}_products.csv")
    if not os.path.exists(file_path):
        logger.error(f"Supplier data not found for: {supplier_name}")
        raise HTTPException(status_code=404, detail="Supplier data not found.")

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            data = [row for row in reader]
            headers = reader.fieldnames  # Get headers from the DictReader
            return {"headers": headers, "data": data}
    except Exception as e:
        logger.error(f"Error reading supplier data for {supplier_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading supplier data: {e}")
