import requests
from src.domain.product_price import ProductPrice

class DermaShopScraper:
    BASE_URL = "https://dermashop.pe"
    SEARCH_URL = f"{BASE_URL}/search/suggest.json"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
    })
        
    def search(self, query: str) -> list[ProductPrice]:
        params = {
            "q": query,
            "resources[type]": "product"
        }

        response = self.session.get(self.SEARCH_URL, params=params, timeout=(5, 15))
        response.raise_for_status()

        data = response.json()
        products = data.get("resources", {}).get("results", {}).get("products", [])
        results = []

        for item in products:
            name = item.get("title")
            original_price = item.get("compare_at_price_max")
            final_discount_price = item.get("price")
            available = item.get("available")
            relative_url = item.get("url")

            product_url = f"{self.BASE_URL}{relative_url}" if relative_url else self.BASE_URL

            results.append(ProductPrice(
                store="Dermashop",
                product_name=name,
                original_price=float(original_price) if original_price else None,
                discount_price= None,
                final_discount_price=final_discount_price,
                currency="PEN",
                url=product_url,
                sku=None,
                availability="En stock" if available else "Sin stock"
            ))
        
        return results



