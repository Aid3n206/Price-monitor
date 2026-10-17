"""Simple CSV + in-memory history. Move to SQLite if you >1000 items."""
import csv
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = DATA_DIR / "products.csv"

def append_row(product) -> None:
    write_header = not OUTPUT_FILE.exists()
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow([
                "timestamp", "source_url", "title", "price", "currency",
                "stock", "condition", "confidence"
            ])
        writer.writerow([
            product.extracted_at, product.source_url, product.title,
            product.price, product.currency, product.stock, product.condition,
            product.confidence,
        ])