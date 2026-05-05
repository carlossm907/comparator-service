def deduplicate_products(products):
    unique, seen = [], set()
    for p in products:
        key = (p.store, p.product_name.strip().lower(), p.url.strip().lower())
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique

def get_top_per_store(scored_by_store, top_n=3):
    final = []
    for store, items in scored_by_store.items():
        if not items:
            continue
        items.sort(key=lambda x: x[1], reverse=True)
        final.extend([p for p, _ in items[:top_n]])
    return final


def scrape_inkafarma_and_mifarma(algolia, inkafarma, mifarma, alias):
    ids = algolia.search_ids(alias)
    return inkafarma.search_by_ids(ids) + mifarma.search_by_ids(ids)