import csv
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def load_subscribers(filepath="subscribers.csv"):
    subscribers = []
    with open(filepath) as f:
        for row in csv.DictReader(f):
            if row["active"].strip().lower() == "true":
                subscribers.append(row)
    return subscribers

def build_html(new_items: list, updated_items: list):
    date_str = datetime.now().strftime("%Y-%m-%d")
    html = f"<h2>AWS What's New — {date_str}</h2>"

    if new_items:
        html += "<h3>🆕 신규</h3><ul>"
        for item in new_items:
            html += f'<li><a href="{item["link"]}">{item["title"]}</a><br>{item["summary"]}</li><br>'
        html += "</ul>"

    if updated_items:
        html += "<h3>🔄 업데이트</h3><ul>"
        for item in updated_items:
            html += f'<li><a href="{item["link"]}">{item["title"]}</a><br>'
            html += f'<b>변경 전:</b> {item["prev_summary"]}<br>'
            html += f'<b>변경 후:</b> {item["summary"]}</li><br>'
        html += "</ul>"

    if not new_items and not updated_items:
        html += "<p>오늘 새로운 항목이 없습니다.</p>"

    return html

def send_digest(new_items: list, updated_items: list):
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