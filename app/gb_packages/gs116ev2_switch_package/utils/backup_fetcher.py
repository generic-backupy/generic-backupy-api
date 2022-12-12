import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

class BackupFetcher:
    @staticmethod
    def fetch_backup(temp_path: str, host: str, password: str, switch_type: str,
                     login_input_id: str, login_button_id: str,
                     backup_endpoint: str, timeout=60):
        options = Options()
        prefs = {"download.default_directory" : temp_path}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome("chromedriver", options=options)

        driver.get(f"http://{ host }/login.htm")
        time.sleep(2)
        driver.find_element('id', login_input_id).send_keys(password)
        driver.find_element('id', login_button_id).click()
        time.sleep(2)
        driver.get(f"http://{ host }/{backup_endpoint}")

        # wait for the download
        seconds = 0
        while seconds <= timeout:
            time.sleep(1)
            finished = True
            listdir = os.listdir()
            if len(listdir) == 0:
                break
            for file in listdir:
                if file.endswith(".crdownload"):
                    finished = False
            if finished:
                break
            seconds += 1
