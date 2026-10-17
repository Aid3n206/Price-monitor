"""Turn raw HTML into compact, LLM-friendly text (selectors, whitespace)."""
from bs4 import BeautifulSoup
from dataclasses import dataclass


def clean_html(html: str, selectors: list = None) -> str:
    if not html:
        return ""

    soup = BeautifulSoup(html, "lxml")
    # prefer selectors if they exist
    chunks = []
    if selectors:
        for sel in selectors:
            try:
                chunks.extend([n.get_text(" ", strip=True) for n in soup.select(sel)])
            except Exception:
                continue
    # fallback: body text
    if not chunks:
        chunks = [soup.get_text(" ", strip=True)]

    text = "\n".join(chunks)
    # Collapse all whitespace into single spaces for LLM-friendly compact text
    import re
    text = re.sub(r"\s+", " ", text).strip()
    # Cap to ~6k chars for cheap models
    return text[:6000]