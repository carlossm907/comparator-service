import requests

class AlgoliaSearch:
    ALGOLIA_URL = "https://15w622laq4-dsn.algolia.net/1/indexes/products/query"

    HEADERS = {
            "X-Algolia-API-Key": "3ba15abece13b00b123c5501680690f7",
            "X-Algolia-Application-Id": "15W622LAQ4",
            "Content-Type": "application/json",
    }

    def __init__(self):
        self.session = requests.Session()

    def search_ids(self, query: str) -> list[str]:

        payload = {
            "params": f"query={query}&hitsPerPage=20"
        }
        
        response = self.session.post(self.ALGOLIA_URL, json=payload, headers=self.HEADERS, timeout=(5, 15))
        response.raise_for_status()

        data = response.json()
        ids = []

        for hit in data.get("hits", []):
            product_id = hit.get("objectID")
            if product_id:
                ids.append(product_id)
        
        return ids




