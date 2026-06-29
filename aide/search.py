"""
aide/search.py — One-time writeup context loader.

Searches DuckDuckGo for writeups/walkthroughs for the given CTF room,
fetches & scrapes the top pages, and returns a combined plain-text
context string (max ~6000 chars) that is stored in memory for the
entire TUI session.
"""

import asyncio
from typing import Optional

import httpx
from bs4 import BeautifulSoup
from ddgs import DDGS

# How many search results to try fetching full content from
MAX_RESULTS = 4

# Maximum chars to keep from each fetched page
MAX_CHARS_PER_PAGE = 2000

# Total combined context cap (stays inside LLM context window)
MAX_TOTAL_CHARS = 7000

# Domains known to have good CTF writeups — prioritised via query hints
WRITEUP_SITES = [
    "site:medium.com",
    "site:github.com",
    "site:hackthebox.com",
    "site:tryhackme.com",
    "site:infosecwriteups.com",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}


def _build_query(platform: str, room: str, mode: str) -> str:
    """Build a focused DuckDuckGo query for the room."""
    base = f"{platform} {room} writeup walkthrough"
    if mode == "ctf":
        base += " CTF solution"
    elif mode == "web":
        base += " web exploitation"
    elif mode == "network":
        base += " network enumeration"
    elif mode == "scripting":
        base += " script automation"
    return base


def _extract_text(html: str) -> str:
    """Strip HTML tags and return readable plain text."""
    soup = BeautifulSoup(html, "html.parser")
    # Remove noise elements
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # Collapse excessive blank lines
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return "\n".join(lines)


async def _fetch_page(client: httpx.AsyncClient, url: str) -> str:
    """Fetch a URL and return stripped plain text, or empty string on error."""
    try:
        resp = await client.get(url, headers=HEADERS, follow_redirects=True, timeout=10.0)
        if resp.status_code == 200 and "text/html" in resp.headers.get("content-type", ""):
            return _extract_text(resp.text)[:MAX_CHARS_PER_PAGE]
    except Exception:
        pass
    return ""


async def fetch_room_context(platform: str, room: str, mode: str) -> tuple[str, list[str]]:
    """
    Search for writeups and return:
      - A combined context string to inject into LLM prompts.
      - A list of source URLs that were successfully fetched.

    Returns ("", []) if no useful content could be found.
    """
    query = _build_query(platform, room, mode)

    # Run DuckDuckGo search in a thread (DDGS is sync)
    loop = asyncio.get_event_loop()
    try:
        results: list[dict] = await loop.run_in_executor(
            None,
            lambda: list(DDGS().text(query, max_results=MAX_RESULTS)),
        )
    except Exception:
        return "", []

    if not results:
        return "", []

    urls = [r["href"] for r in results if r.get("href")]
    snippets_only = [r.get("body", "") for r in results]

    # Try to fetch full page content for each URL
    async with httpx.AsyncClient() as client:
        tasks = [_fetch_page(client, url) for url in urls]
        pages = await asyncio.gather(*tasks)

    # Combine: prefer full page, fall back to snippet
    parts: list[str] = []
    loaded_urls: list[str] = []
    total = 0

    for url, page_text, snippet in zip(urls, pages, snippets_only):
        content = page_text if page_text else snippet
        if not content:
            continue
        chunk = f"--- Source: {url} ---\n{content}\n"
        if total + len(chunk) > MAX_TOTAL_CHARS:
            break
        parts.append(chunk)
        loaded_urls.append(url)
        total += len(chunk)

    combined = "\n".join(parts)
    return combined, loaded_urls
