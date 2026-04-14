
import requests
from bs4 import BeautifulSoup
import hashlib
import os

URL = "https://www.stoneyacrepuppies.ca/ready-for-reservation.html"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_msg(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_content():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text(" ", strip=True)

def get_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

def main():
    content = get_content()
    new_hash = get_hash(content)

    if os.path.exists("last.txt"):
        with open("last.txt", "r") as f:
            old_hash = f.read()
    else:
        old_hash = ""

    if old_hash and new_hash != old_hash:
        send_msg("🐶 网站更新了")

    with open("last.txt", "w") as f:
        f.write(new_hash)

if __name__ == "__main__":
    main()
