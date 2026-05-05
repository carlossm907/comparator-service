def deduplicate_products(products):
    unique, seen = [], set()
    for p in products:
        key = (p.store, p.product_name.strip().lower(), p.url.strip().lower())
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique