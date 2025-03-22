import os
import requests
import time
import logging
import schedule
import hashlib
import sys
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
FIA_URL = os.getenv("FIA_URL")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 5))  # Minutes
SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", 60))  # Seconds

TELEGRAM_BOT_API = f"https://api.telegram.org/bot{os.getenv('TOKEN')}/sendMessage"

# Logging configuration
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG, handlers=[logging.StreamHandler(sys.stdout)], encoding='utf-8')
#logging.basicConfig(format='%(asctime)s %(message)s', filename='fia_bot.log', level=logging.INFO, encoding='utf-8')
logger = logging.getLogger('fia_bot')

# Store last known hash value
LAST_HASH = None
LAST_PAGE_CONTENT = None

def make_request(url):
    """Send a GET request to the FIA website."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"make_request: Request failed: {e}")
        return None

def send_telegram_message(text):
    """Send a message to the Telegram group."""
    try:
        response = requests.post(TELEGRAM_BOT_API, data={"chat_id": GROUP_CHAT_ID, "text": text})
        logger.info(f"send_telegram_message: Message sent: {text}, Telegram response: {response.text}")
    except requests.RequestException as e:
        logger.error(f"send_telegram_message: Failed to send message to Telegram: {e}")

def get_page_hash(html):
    """Generate a hash of the page content."""
    return hashlib.md5(html.encode("utf-8")).hexdigest()

def check_for_new_results():
    """Check the FIA website for updates using a hash-based comparison."""
    global LAST_HASH
    global LAST_PAGE_CONTENT

    logger.info("check_for_new_results: Checking FIA website for updates")
    html = make_request(FIA_URL)
    if not html:
        return

    page_hash = get_page_hash(html)
    logger.info(f"check_for_new_results: Last hash: {LAST_HASH}, Current hash: {page_hash}")

    if LAST_HASH is None:
        LAST_HASH = page_hash
        logger.info("check_for_new_results: Initial page hash stored")
        return

    if page_hash != LAST_HASH:
        LAST_HASH = page_hash
        send_telegram_message(f"🆕 FIA website has been updated: {FIA_URL}")
        logger.info("check_for_new_results: Website content changed. Notification sent")
        soup = BeautifulSoup(html, "html.parser")
        new_page_content = soup.prettify()
        if LAST_PAGE_CONTENT:
            diff = difflib.unified_diff(
                LAST_PAGE_CONTENT.splitlines(),
                new_page_content.splitlines(),
                lineterm=""
            )
            diff_text = "\n".join(diff)
            if diff_text:
                logger.info("Differences found:\n" + diff_text)
        LAST_PAGE_CONTENT = new_page_content

def scheduled_task():
    """Schedule the task to run at a fixed interval."""
    schedule.every(CHECK_INTERVAL).minutes.do(check_for_new_results)
    logger.info("scheduled_task: Monitoring started, interval: %d minutes", CHECK_INTERVAL)

    while True:
        schedule.run_pending()
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    logger.info("Starting FIA monitoring bot...")
    scheduled_task()
