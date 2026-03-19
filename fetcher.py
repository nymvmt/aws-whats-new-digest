import feedparser
from datetime import datetime, timezone
import re
import json, time, os
from pathlib import Path
import certifi
import requests
import urllib.request

def strip_html(text: str) -> str:
    clean = re.sub(r"<[^>]+>", "", text or "")
    return clean.strip()
    

FEED_URL = "https://aws.amazon.com/ko/about-aws/whats-new/recent/feed/"

def _debug_log(message: str, data: dict, *, run_id: str, hypothesis_id: str, location: str):
    payload = {
        "sessionId": "498edb",
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    # Try local file append first (preferred for Python)
    try:
        log_path = Path(__file__).resolve().parent / ".cursor" / "debug-498edb.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return
    except Exception:
        pass
    # Fallback to local debug ingest endpoint (works even if filesystem writes are restricted)
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:7932/ingest/55503be4-f3d6-4928-8ef8-e75915b55859",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json", "X-Debug-Session-Id": "498edb"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=2).read()
    except Exception:
        pass

def fetch_items():
    run_id = os.getenv("DEBUG_RUN_ID", "local")
    _debug_log(
        "fetch_items start",
        {
            "feed_url": FEED_URL,
            "http_proxy_set": bool(os.getenv("HTTP_PROXY") or os.getenv("http_proxy")),
            "https_proxy_set": bool(os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")),
            "all_proxy_set": bool(os.getenv("ALL_PROXY") or os.getenv("all_proxy")),
            "no_proxy_set": bool(os.getenv("NO_PROXY") or os.getenv("no_proxy")),
        },
        run_id=run_id,
        hypothesis_id="H1",
        location="fetcher.py:fetch_items:start",
    )
    feed = feedparser.parse(FEED_URL)
    if bool(getattr(feed, "bozo", False)) and "CERTIFICATE_VERIFY_FAILED" in str(getattr(feed, "bozo_exception", "")):
        _debug_log(
            "urllib cert verify failed; retrying via requests+certifi",
            {},
            run_id=run_id,
            hypothesis_id="H3",
            location="fetcher.py:fetch_items:cert_retry",
        )
        try:
            resp = requests.get(
                FEED_URL,
                timeout=30,
                headers={"User-Agent": "aws-whats-new-digest/1.0"},
                verify=certifi.where(),
            )
            _debug_log(
                "requests fetch done",
                {"status_code": resp.status_code, "bytes": len(resp.content or b"")},
                run_id=run_id,
                hypothesis_id="H3",
                location="fetcher.py:fetch_items:requests_done",
            )
            resp.raise_for_status()
            feed = feedparser.parse(resp.content)
        except Exception as e:
            _debug_log(
                "requests fallback failed",
                {"error": str(e)[:200]},
                run_id=run_id,
                hypothesis_id="H3",
                location="fetcher.py:fetch_items:requests_failed",
            )
    _debug_log(
        "feed parsed",
        {
            "entries_len": len(getattr(feed, "entries", []) or []),
            "bozo": bool(getattr(feed, "bozo", False)),
            "bozo_exception": str(getattr(feed, "bozo_exception", ""))[:200],
            "status": feed.get("status"),
            "href": getattr(feed, "href", None),
        },
        run_id=run_id,
        hypothesis_id="H2",
        location="fetcher.py:fetch_items:after_parse",
    )
    items = []
    for entry in feed.entries:
        entry_id = getattr(entry, "id", None) or getattr(entry, "link", None) or getattr(entry, "title", None)
        if not entry_id:
            continue
        published_parsed = getattr(entry, "published_parsed", None)
        if published_parsed:
            published = datetime(*published_parsed[:6], tzinfo=timezone.utc).isoformat()
        else:
            published = datetime.now(timezone.utc).isoformat()
        items.append({
            "id": entry_id,
            "title": getattr(entry, "title", "") or "",
            "link": getattr(entry, "link", "") or "",
            "summary": strip_html(entry.get("summary", "")),
            "published": published
        })
    return items

