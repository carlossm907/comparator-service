from dataclasses import dataclass


@dataclass
class MatchResult:
    kardex_name: str
    scraped_name: str
    store: str
    score: float
    status: str
    brand_match: bool
    volume_match: bool