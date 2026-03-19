import feedparser
from datetime import datetime, timezone
from html.parser import HTMLParser
import re

def strip_html(text: str) -> str:
      clean = re.sub(r'<[^>]+>', '', text)
      return clean.strip()
    

FEED_URL = "https://aws.amazon.com/ko/about-aws/whats-new/recent/feed/"

def fetch_items():
    feed = feedparser.parse(FEED_URL)
    items = []
    for entry in feed.entries:
        items.append({
            "id": entry.id,
            "title": entry.title,
            "link": entry.link,
            "summary": strip_html(entry.get("summary", "")),
            "published": datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat()
        })
    return items

