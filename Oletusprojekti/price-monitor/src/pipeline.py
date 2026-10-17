"""Run all targets: fetch -> clean -> AI extract -> store. Keeps cost logs."""
import json
import sys

from src.config import TARGETS, REQUEST_MIN_DELAY_SEC
from src.fetch import fetch_url
from src.clean import clean_html
from src.extract import extract_product
from src.storage import append_row

def main():
    budget_pages = 0
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        print("DRY RUN: no LLM calls (showing prompts only)")
        for t in TARGETS:
            print(f"[target] {t['label']} :: {t['url']}")
        return

    for i, target in enumerate(TARGETS, start=1):
        print(f"\n[{i}/{len(TARGETS)}] {target['label']}")
        page = fetch_url(target["url"], min_delay=REQUEST_MIN_DELAY_SEC)
        if page.status >= 400 or not page.html:
            print(f"  fetch failed: {page.status} {page.reason}")
            continue

        body = clean_html(page.html, selectors=target.get("selectors"))
        print(f"  compact body length: {len(body)} chars")

        try:
            product = extract_product(target["url"], target["fields"], body)
            append_row(product)
            print(f"  extracted: {product.title} | {product.price} {product.currency} | {product.stock} (conf={product.confidence:.2f})")
        except Exception as e:
            print(f"  extraction failed: {e}")

    print("\nDone. Check data/products.csv")

if __name__ == "__main__":
    main()