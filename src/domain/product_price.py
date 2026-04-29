from dataclasses import dataclass
from typing import Optional

@dataclass
class ProductPrice:
    store: str
    product_name: str

    original_price: Optional[float]
    discount_price: Optional[float]
    final_discount_price: Optional[float]

    currency: str
    url: str

    sku: Optional[str] = None
    availability: Optional[str] = None