import re
from typing import Optional
from unidecode import unidecode
from rapidfuzz import fuzz

from src.domain.match_result import MatchResult

KNOWN_BRANDS = [
    "svr", "isdin", "isdinceutics", "uriage", "vichy", "la roche posay",
    "bioderma", "frezyderm", "esthederm", "isispharma", "babe", "babé",
    "differin", "pilexil", "tizo", "meline", "fisiogel", "normaderm",
    "neotone", "acniben", "umbrella", "daeha", "bariéderm", "bariederm",
    "alitopic", "nutratopic", "timofree", "hyalix", "kirupro",
]

VOLUME_PATTERN = re.compile(
    r'(\d+[\.,]?\d*\s*(?:ml|gr|g|mg|l|un|cap|caps|capsulas))',
    re.IGNORECASE
)

NOISE_WORDS = {
    "almacen", "alamacen", "almacén", "todos", "formulados",
    "nuevo", "nueva", "x", "fco", "frasco", "crema",
}

class ProductMatcher:
    def __init__(self, kardex_products: list[str]):
        self.kardex_index = [
            self._tokenize(p) for p in kardex_products
        ]
        self.kardex_originals = kardex_products

    def _normalize(self, text: str) -> str:
        text = unidecode(text.lower())
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _extract_volumes(self, text: str) -> set[str]:
        return {
            re.sub(r'\s', '', v.lower())
            for v in VOLUME_PATTERN.findall(text)
        }

    def _extract_brand(self, text: str) -> Optional[str]:

        norm = self._normalize(text)
        for brand in sorted(KNOWN_BRANDS, key=len, reverse=True):
            if brand in norm:
                return brand
        return None

    def _clean_core(self, text: str) -> str:
        norm = self._normalize(text)

        norm = VOLUME_PATTERN.sub(' ', norm)

        brand = self._extract_brand(norm)
        if brand:
            norm = norm.replace(brand, ' ')

        tokens = [w for w in norm.split() if w not in NOISE_WORDS]

        tokens = [t for t in tokens if len(t) > 2 or t in ('spf', 'fps')]

        return ' '.join(tokens)

    def _tokenize(self, text: str) -> dict:
        return {
            "original": text,
            "brand": self._extract_brand(text),
            "volumes": self._extract_volumes(text),
            "core": self._clean_core(text),
        }


    def _compute_score(self, tokens_a: dict, tokens_b: dict) -> float:

        name_score = fuzz.token_set_ratio(tokens_a["core"], tokens_b["core"])

        brand_match = (
            tokens_a["brand"] is not None
            and tokens_a["brand"] == tokens_b["brand"]
        )
        brand_score = 100 if brand_match else (
            50 if (tokens_a["brand"] is None or tokens_b["brand"] is None) else 0
        )

        vol_a, vol_b = tokens_a["volumes"], tokens_b["volumes"]
        if not vol_a and not vol_b:
            vol_score = 80  
        elif vol_a & vol_b:
            vol_score = 100 
        elif not vol_a or not vol_b:
            vol_score = 60  
        else:
            vol_score = 0    

        return 0.60 * name_score + 0.20 * brand_score + 0.20 * vol_score



    def find_match(
        self,
        scraped_name: str,
        store: str = "",
        threshold_match: float = 85,
        threshold_review: float = 60,
    ) -> MatchResult:

        tokens_scraped = self._tokenize(scraped_name)

        best_score = 0.0
        best_idx = 0

        for i, tokens_kardex in enumerate(self.kardex_index):
            score = self._compute_score(tokens_kardex, tokens_scraped)
            if score > best_score:
                best_score = score
                best_idx = i

        best = self.kardex_index[best_idx]

        if best_score >= threshold_match:
            status = "match"
        elif best_score >= threshold_review:
            status = "review"
        else:
            status = "discard"

        return MatchResult(
            kardex_name=self.kardex_originals[best_idx],
            scraped_name=scraped_name,
            store=store,
            score=round(best_score, 1),
            status=status,
            brand_match=(best["brand"] == tokens_scraped["brand"]),
            volume_match=bool(best["volumes"] & tokens_scraped["volumes"]),
        )

    def match_all(
        self,
        scraped_products,   
        threshold_match: float = 85,
        threshold_review: float = 60,
    ) -> list[MatchResult]:

        results = []
        for product in scraped_products:
            result = self.find_match(
                scraped_name=product.product_name,
                store=product.store,
                threshold_match=threshold_match,
                threshold_review=threshold_review,
            )
            results.append(result)
        return results
