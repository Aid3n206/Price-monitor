"""Fetch web pages politely. Uses requests; add Playwright later if site is JS-rendered."""
import time
import random
from dataclasses import dataclass

import requests
from collections import Counter

# Basic rotating UA list to avoid easy bot detections (low-tech resume)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/18.0 Safari/605.1.15",
]

@dataclass
class Page:
    url: str
    html: str
    status: int
    reason: str = ""

def fetch_url(url: str, timeout: float = 15.0, min_delay: float = 1.0) -> Page:
    """Fetch a single URL with retry on transient failures."""
    delay = min_delay + random.random() * 0.5
    time.sleep(delay)  # be polite; adjust after measuring

    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}

    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            resp.encoding = resp.apparent_encoding or "utf-8"
            resp.raise_for_status()
            return Page(url=url, html=resp.text, status=resp.status_code)
        except requests.RequestException as e:
            if attempt == 2:
                return Page(url=url, html="", status=getattr(e.response, "status_code", -1), reason=str(e))
            time.sleep(2 ** attempt)
    return Page(url=url, html="", status=-1, reason="unknown")