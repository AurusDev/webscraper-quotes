import asyncio
import logging
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup
import json
import csv

BASE_URL = "https://quotes.toscrape.com/"

@dataclass
class Quote:
    text: str
    author: str
    tags: List[str]

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )

def parse_quotes_page(html: str, current_url: str) -> Tuple[List[Quote], Optional[str]]:
    soup = BeautifulSoup(html, "lxml")
    quotes: List[Quote] = []
    for block in soup.select("div.quote"):
        text = block.select_one("span.text").get_text(strip=True).strip("“”\"'")
        author = block.select_one("small.author").get_text(strip=True)
        tags = [t.get_text(strip=True) for t in block.select("div.tags a.tag")]
        quotes.append(Quote(text=text, author=author, tags=tags))
    next_el = soup.select_one("li.next a[href]")
    next_url = urljoin(current_url, next_el["href"]) if next_el else None
    return quotes, next_url

async def fetch_html(client: httpx.AsyncClient, url: str) -> Optional[str]:
    try:
        resp = await client.get(url, timeout=10.0)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logging.error("Erro ao buscar %s: %s", url, e)
        return None

async def crawl_all_quotes(start_url: str = BASE_URL, max_pages: Optional[int] = None) -> List[Quote]:
    setup_logging()
    quotes: List[Quote] = []
    async with httpx.AsyncClient(headers={"User-Agent": "Mozilla/5.0"}) as client:
        url = start_url
        page = 0
        while url:
            page += 1
            if max_pages and page > max_pages:
                break
            html = await fetch_html(client, url)
            if not html:
                break
            q, next_url = parse_quotes_page(html, url)
            quotes.extend(q)
            url = next_url
    return quotes

def save_to_json(quotes: List[Quote], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(q) for q in quotes], f, ensure_ascii=False, indent=2)

def save_to_csv(quotes: List[Quote], path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "author", "tags"])
        for q in quotes:
            writer.writerow([q.text, q.author, "|".join(q.tags)])
