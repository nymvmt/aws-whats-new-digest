import feedparser
from datetime import datetime, timezone

FEED_URL = "https://aws.amazon.com/ko/about-aws/whats-new/recent/feed/"

def fetch_items():
    feed = feedparser.parse(FEED_URL)
    items = []
    for entry in feed.entries:
        items.append({
            "id": entry.id,
            "title": entry.title,
            "link": entry.link,
            "summary": entry.get("summary", ""),
            "published": datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat()
        })
    return items