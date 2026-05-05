from typing import Optional


def to_float(value) -> Optional[float]:
    if value is None:
        return None
    try:
        f = float(value)
        if f > 10_000:
            f = f / 100
        return f
    except (ValueError, TypeError):
        return None


def fmt_price(value) -> str:
    f = to_float(value)
    if f is None or f == 0:
        return "     —"
    return f"S/ {f:>7.2f}"
