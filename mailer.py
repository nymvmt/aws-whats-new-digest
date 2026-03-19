import csv
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from category_rules import get_category

def load_subscribers(filepath="subscribers.csv"):
    subscribers = []
    with open(filepath) as f:
        for row in csv.DictReader(f):
            if row["active"].strip().lower() == "true":
                subscribers.append(row)
    return subscribers

def build_html(new_items: list, updated_items: list):
    date_str = datetime.now().strftime("%Y-%m-%d")

    style = """
    <style>
        body { font-family: Arial, sans-serif; color: #333; max-width: 800px; margin: 0 auto; }
        h2 { background-color: #232f3e; color: white; padding: 12px 16px; border-radius: 4px; }
        h3 { color: #232f3e; border-bottom: 2px solid #232f3e; padding-bottom: 4px; }
        .item { border-bottom: 1px solid #e0e0e0; padding: 12px 0; }
        .item:last-child { border-bottom: none; }
        .item a { font-weight: bold; color: #0073bb; text-decoration: none; }
        .category { display: inline-block; background: #f0f0f0; border-radius: 3px;
                    padding: 2px 8px; font-size: 12px; color: #666; margin-bottom: 4px; }
        .highlight-new { background-color: #e6f4ea; padding: 8px; border-left: 4px solid #34a853; border-radius: 2px; }
        .highlight-updated { background-color: #fff8e1; padding: 8px; border-left: 4px solid #fbbc04; border-radius: 2px; }
        .diff-before { color: #999; text-decoration: line-through; font-size: 13px; }
        .diff-after { color: #333; font-size: 13px; }
    </style>
    """

    # 카테고리 목록 수집
    all_groups = {}
    for item in new_items:
        cat = get_category(item["title"])
        all_groups.setdefault(cat, True)
    for item in updated_items:
        cat = get_category(item["title"])
        all_groups.setdefault(cat, True)

    # 카테고리별 아이템 수 집계
    cat_counts = {}
    for item in new_items:
        cat = get_category(item["title"])
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

  # 네비게이션 바
    nav = '<div style="background:#f5f5f5; padding:12px 16px; border-radius:4px; margin-bottom:16px; line-height:2;">'
    for cat, count in cat_counts.items():
        nav += f'<span style="margin-right:12px; font-size:13px; color:#333;">#{cat} <span style="background:#34a853; color:white; border-radius:10px; padding:1px 7px; font-size:11px;">{count}</span></span>'
    nav += '</div>'

    html = f"{style}<h2>AWS What's New — {date_str}</h2>{nav}"

    # 신규 항목
    if new_items:
        groups = {}
        for item in new_items:
            cat = get_category(item["title"])
            groups.setdefault(cat, []).append(item)

        html += "<h3>🆕 신규</h3>"
        for cat, items in groups.items():
            anchor = cat.replace(" ", "-").replace("/", "")
            html += f'<h4 id="{anchor}">{cat} ({len(items)})</h4>'
            for item in items:
                html += f"""
                <div class="item">
                    <div class="highlight-new">
                        <a href="{item['link']}">{item['title']}</a><br>
                        <span class="diff-after">{item['summary']}</span>
                    </div>
                </div>"""

    # 업데이트 항목
    if updated_items:
        groups = {}
        for item in updated_items:
            cat = get_category(item["title"])
            groups.setdefault(cat, []).append(item)

        html += "<h3>🔄 업데이트</h3>"
        for cat, items in groups.items():
            anchor = cat.replace(" ", "-").replace("/", "")
            html += f'<h4 id="{anchor}">{cat} ({len(items)})</h4>'
            for item in items:
                html += f"""
                <div class="item">
                    <div class="highlight-updated">
                        <a href="{item['link']}">{item['title']}</a><br>
                        <span class="diff-before">{item.get('prev_summary', '')}</span><br>
                        <span class="diff-after">→ {item['summary']}</span>
                    </div>
                </div>"""

    return html

def send_digest(new_items: list, updated_items: list):
    if not new_items and not updated_items:
        print("새로운 항목 없음. 메일 발송 생략.")
        return

    subscribers = load_subscribers()
    if not subscribers:
        print("구독자 없음. 발송 생략.")
        return

    EMAIL_FROM = os.environ["EMAIL_FROM"]
    EMAIL_PASS = os.environ["EMAIL_PASS"]
    subject = f"[AWS 새소식] {datetime.now().strftime('%Y-%m-%d')} 다이제스트"
    html_body = build_html(new_items, updated_items)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASS)

        for sub in subscribers:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = EMAIL_FROM
            msg["To"] = sub["email"]
            msg.attach(MIMEText(html_body, "html"))
            server.sendmail(EMAIL_FROM, sub["email"], msg.as_string())
            print(f"발송 완료: {sub['email']}")