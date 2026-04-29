import requests
from src.domain.product_price import ProductPrice

class MifarmaScraper:
    BASE_URL = "https://mifarma.com.pe"
    API_URL = "https://5doa19p9r7.execute-api.us-east-1.amazonaws.com/MMMFPRD"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Origin": "https://mifarma.pe",
            "Referer": "https://mifarma.pe/",
        })
    
    def search_by_ids(self, ids: list[str]) -> list[ProductPrice]:
        if not ids:
            return []

        ids = ids[:10]
        return self.get_products_by_ids(ids)

    def get_products_by_ids(self, ids: list[str]) -> list[ProductPrice]:
        ids_str = ",".join(ids)

        url = f"{self.API_URL}/products/{ids_str}"

        params = {
            "companyCode": "MF",
            "saleChannel": "WEB",
            "saleChannelType": "DIGITAL",
            "sourceDevice": "null",
            "userCallCenterId": "undefined"
        }

        response = self.session.get(url, params=params, timeout=(5, 15))
        response.raise_for_status()

        data = response.json()
    
        results = []

        for item in data:
            name = item.get("name")
            original_price = item.get("price")
            discount_price = item.get("priceAllPaymentMethod")
            final_discount_price = item.get("priceWithpaymentMethod")
            stock = item.get("stock")
            slug = item.get("slug")
            sku = item.get("id")

            product_url = f"{self.BASE_URL}/producto/{slug}/{sku}"

            results.append(ProductPrice(
                store="Mifarma",
                product_name=name,
                original_price=original_price,
                discount_price=discount_price,
                final_discount_price=final_discount_price,
                currency="PEN",
                url=product_url,
                sku=sku,
                availability="En stock" if stock > 0 else "Sin stock"
            ))

        return results

        