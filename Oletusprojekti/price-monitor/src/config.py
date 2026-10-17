# Replace with 2-3 real public product pages when ready. These demo pages are stable and public.
TARGETS = [
    {
        "label": "Books to Scrape - A Light in the Attic",
        "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        "fields": ["title", "price", "currency", "stock", "condition"],
        # Optional CSS hints help the LLM find sections fast.
        "selectors": ["h1", ".price_color", ".instock.availability", "#product_description ~ p"],
    },
    {
        "label": "Books to Scrape - Tipping the Velvet",
        "url": "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
        "fields": ["title", "price", "currency", "stock", "condition"],
        "selectors": ["h1", ".price_color", ".instock.availability", "#product_description ~ p"],
    },
]
# Safety & politeness controls
MAX_PAGES = 4
REQUEST_MIN_DELAY_SEC = 1.0