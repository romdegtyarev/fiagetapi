################################################################################
################################################################################
import requests
import datetime
import schedule
import time
from pdf2image import convert_from_path
from datetime import date
from bs4 import BeautifulSoup

import config

################################################################################
# Main variables
################################################################################
FIA_URL = "https://www.fia.com/"
FIA_URL_DOCS = "https://www.fia.com/documents/season/season-2023-2042/championships/fia-formula-one-world-championship-14"
RACE_TEMPLATE = "Final Race Classification"
GRID_TEMPLATE = "Final Starting Grid"

TELEGRAM_BOT_API = "https://api.telegram.org/bot"
TELEGRAM_BOT_API_SEND_PHOTO_METHOD = "/sendPhoto?"

# Config
DATABASE_PATH = "/home/fia/fia/fia_get/db/"
DATABASE_NAME = "/home/fia/fia/fia_get/local_database"
SCHEDULED_TASK_DELAY = 60  # Sec
SCHEDULED_TASK_SYNCHRONIZATION_INTERVAL = 240  # Min
GROUP_CHAT_ID = config.chat_id
TOKEN = config.token


################################################################################
# Functions
################################################################################
################################################################################
# name:        
# description: 
################################################################################
def send_photo(file_name, chat_id):
    """

    :param file_name:
    :param chat_id:
    """
    image = open(file_name, "rb")
    # TODO: Check
    url = TELEGRAM_BOT_API + TOKEN + TELEGRAM_BOT_API_SEND_PHOTO_METHOD + "chat_id=" + chat_id
    r = requests.post(url, files={'photo': image})
    print("send_photo: result: ", r.text)


################################################################################
# name:        
# description: 
################################################################################
def convert_save_send_image(in_file_name, out_file_name, page):
    """

    :param in_file_name:
    :param out_file_name:
    :param page:
    """
    images = convert_from_path(in_file_name)
    image_name = DATABASE_PATH + out_file_name + '.jpg'
    images[page].save(image_name, 'JPEG')
    send_photo(image_name, GROUP_CHAT_ID)


################################################################################
# name:        
# description: 
################################################################################
def download_pdf(url, file_name, headers):
    """

    :param url:
    :param file_name:
    :param headers:
    """
    # Send GET request
    response = requests.get(url, headers=headers)
    # Save the PDF
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
    else:
        print("download_pdf: ", response.status_code)


################################################################################
# name:        
# description: 
################################################################################
def add_to_local_database(site_dates, site_links):
    """

    :param site_dates:
    :param site_links:
    """
    pdf_url = FIA_URL + site_links
    pdf_file_name = DATABASE_PATH + site_dates + ".pdf"
    download_pdf(pdf_url, pdf_file_name, "")
    # TODO: Result

    local_database = open(DATABASE_NAME, "a")
    # TODO: Check result
    local_database.write(str(site_dates) + "\n")
    local_database.close()

    convert_save_send_image(pdf_file_name, site_dates, 1)


################################################################################
# name:        
# description: 
################################################################################
def cmp_with_local_database(site_dates, site_links):
    """

    :param site_dates:
    :param site_links:
    """
    # TODO: Check site_dates len
    local_database = open(DATABASE_NAME, "r")
    # TODO: Check if opened
    local_database_dates = []
    while True:
        line = local_database.readline()
        if not line:
            break
        local_database_dates.append(line.strip())
    local_database.close

    # Get last date
    format = "%d.%m.%y %H:%M"
    count = len(local_database_dates)
    local_database_date_str = "01.01.01 00:00"
    if count > 0:
        local_database_date_str = local_database_dates[len(local_database_dates) - 1]
    local_database_date_object = datetime.datetime.strptime(local_database_date_str, format)

    site_dates.reverse()
    site_links.reverse()
    for i, j in zip(site_dates, site_links):
        site_database_date_str = i
        site_database_link_str = j
        site_database_date_object = datetime.datetime.strptime(site_database_date_str, format)
        if local_database_date_object < site_database_date_object:
            print("cmp_with_local_database: add_to_local_database")
            add_to_local_database(site_database_date_str, site_database_link_str)


################################################################################
# name:        update_info_from_site
# description: 
################################################################################
def update_info_from_site():
    """
    Update info from site
    """
    print("update_info_from_site: start")
    url = FIA_URL_DOCS
    # TODO: Check response
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    docs = soup.find_all("li", "document-row")

    result_links = []
    result_dates = []
    for i in docs:
        if not RACE_TEMPLATE in i.text:
            if GRID_TEMPLATE not in i.text:
                continue
        docs_race_link_with_tags = i.find("a")
        docs_race_link = docs_race_link_with_tags.get("href")

        docs_race_date_with_tag = docs_race_link_with_tags.find("div", "published")
        docs_race_date = docs_race_date_with_tag.find("span", "date-display-single")

        docs_race_link_str = str(docs_race_link)
        docs_race_date_str = str(docs_race_date.text)

        result_links.append(docs_race_link_str)
        result_dates.append(docs_race_date_str)

    # print("update_info_from_site: dates: ", result_dates, "links: ", result_links)
    cmp_with_local_database(result_dates, result_links)


################################################################################
# name:        scheduled_task
# description: Task for scheduled routine
################################################################################
def scheduled_task():
    """
    Scheduled task
    """
    schedule.every(SCHEDULED_TASK_SYNCHRONIZATION_INTERVAL).minutes.do(update_info_from_site)
    print("scheduled_task: Start")
    while True:
        print("scheduled_task: while")
        schedule.run_pending()
        time.sleep(SCHEDULED_TASK_DELAY)


################################################################################
# Main
################################################################################
def main():
    """
    Main
    """
    print("Starting FIA GET BOT")
    scheduled_task()


if __name__ == "__main__":
    main()
