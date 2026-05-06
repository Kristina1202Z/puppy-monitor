import requests
from bs4 import BeautifulSoup
import hashlib
import os
import smtplib
from email.mime.text import MIMEText

URL = "https://www.stoneyacrepuppies.ca/ready-for-reservation.html"
HASH_FILE = "last.txt"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")


def send_msg(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram skipped: missing BOT_TOKEN or CHAT_ID")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    for chat_id in CHAT_ID.split(","):
        chat_id = chat_id.strip()
        if not chat_id:
            continue

        r = requests.post(
            url,
            data={"chat_id": chat_id, "text": msg},
            timeout=20
        )
        print("Telegram status:", r.status_code)
        print("Telegram response:", r.text)


def send_email(msg):
    if not EMAIL_USER or not EMAIL_PASS:
        print("Email skipped: missing EMAIL_USER or EMAIL_PASS")
        return

    msg_obj = MIMEText(msg, "plain", "utf-8")
    msg_obj["Subject"] = "🐶 Puppy Update!"
    msg_obj["From"] = EMAIL_USER
    msg_obj["To"] = EMAIL_USER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg_obj)

    print("Email sent successfully")


def notify(msg):
    send_msg(msg)
    send_email(msg)


def get_content():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.stoneyacrepuppies.ca/",
        "Connection": "keep-alive",
    }

    r = requests.get(URL, headers=headers, timeout=20)
    print("Page status:", r.status_code)

    if r.status_code == 403:
        notify(f"⚠️ Puppy monitor failed: website blocked GitHub request with 403.\n{URL}")
        raise Exception("403 Forbidden: website blocked GitHub request")

    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(" ", strip=True)
    return text


def get_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def load_old_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def save_new_hash(new_hash):
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        f.write(new_hash)


def main():
    content = get_content()
    new_hash = get_hash(content)
    old_hash = load_old_hash()

    print("Old hash exists:", bool(old_hash))
    print("Old hash:", old_hash)
    print("New hash:", new_hash)

    if old_hash and new_hash != old_hash:
        message = f"🐶 Stoney Acre Puppies 页面更新了！快去看：\n{URL}"
        notify(message)
        print("Update detected and notifications sent")
    elif not old_hash:
        print("First run: saving initial hash only")
    else:
        print("No change detected")

    save_new_hash(new_hash)


if __name__ == "__main__":
    main()
