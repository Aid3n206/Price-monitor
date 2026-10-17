"""AI extraction: send compact page text -> strict JSON schema."""
import json
import os
import re
import time
from dataclasses import dataclass

import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

GROQ_API = os.getenv("GROQ_API_BASE", "https://api.groq.com/openai/v1/chat/completions")
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
API_KEY = os.getenv("GROQ_API_KEY", "")
USE_MOCK = os.getenv("USE_MOCK_EXTRACTOR", "0") == "1"


@dataclass
class Product:
    source_url: str
    title: str = ""
    price: float | None = None
    currency: str = ""
    stock: str = ""
    condition: str = ""
    confidence: float = 0.0
    extracted_at: float = 0.0

PROMPT = """You are a careful data extractor.
Given this web-page text (may be messy), extract only fields I listed. Return compact JSON.
- Title: product name as displayed.
- Price: numeric only (no symbols), null if missing.
- Currency: ISO code if identifiable (USD, EUR), else "".
- Stock: "in-stock", "out-of-stock", "unknown".
- Condition: new/refurb/used/unknown.
- confidence: 0.0-1.0 (low if unsure).

Fields requested: {fields}
Text (truncated):
{body}
JSON schema: {{"title":"","price":null,"currency":"","stock":"","condition":"","confidence":0.0}}"""


def extract_product(source_url: str, fields: list, body_text: str) -> Product:
    if USE_MOCK:
        # Demo fallback: parse the compact page text locally so the output is
        # realistic even without a Groq/OpenAI key. This is NOT AI extraction.
        price_match = re.search(r"([£€$])\s*([0-9][0-9.,]*)", body_text)
        price = None
        currency = ""
        if price_match:
            symbol, amount = price_match.groups()
            currency = {"£": "GBP", "€": "EUR", "$": "USD"}.get(symbol, "")
            try:
                price = float(amount.replace(",", ""))
            except ValueError:
                price = None

        title_match = re.split(r"[£€$]", body_text, maxsplit=1)[0].strip()
        title = title_match[:120] if title_match else f"Demo item from {source_url}"

        stock = "unknown"
        if re.search(r"out of stock|sold out|unavailable", body_text, re.I):
            stock = "out-of-stock"
        elif re.search(r"in stock|available", body_text, re.I):
            stock = "in-stock"

        return Product(
            source_url=source_url,
            title=title or f"Demo item from {source_url}",
            price=price,
            currency=currency,
            stock=stock,
            condition="unknown",
            confidence=0.55,
            extracted_at=time.time(),
        )

    if not API_KEY:
        raise RuntimeError("Missing GROQ_API_KEY. Create .env from .env.example.")

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT.format(fields=fields, body=body_text)}],
        "response_format": {"type": "json_object"},
        "temperature": 0.0,
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    for attempt in range(3):
        try:
            r = requests.post(GROQ_API, json=payload, headers=headers, timeout=30)
            r.raise_for_status()
            data = r.json()["choices"][0]["message"]["content"]
            parsed = json.loads(data)
            return Product(
                source_url=source_url,
                title=parsed.get("title", ""),
                price=parsed.get("price"),
                currency=parsed.get("currency", ""),
                stock=parsed.get("stock", "unknown"),
                condition=parsed.get("condition", "unknown"),
                confidence=float(parsed.get("confidence", 0.0)),
                extracted_at=time.time(),
            )
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(1)