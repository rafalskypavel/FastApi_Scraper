from pydantic import BaseModel
from typing import List, Dict

class SupplierModel(BaseModel):
    base_url: str
    start_page: int
    page_param: str
    template_name: str
    urls: List[str]
    product_card_selector: str
    fields: Dict[str, str]
