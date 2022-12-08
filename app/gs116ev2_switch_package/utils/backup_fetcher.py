import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

class BackupFetcher:
    @staticmethod
    def fetch_backup(temp_path: str, host: str, password: str, timeout=60):
        options = Options()
        prefs = {"download.default_directory" : temp_path}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome("chromedriver", options=options)

        driver.get(f"http://{ host }/login.htm")
        driver.find_element('id', 'passwordtmp').send_keys(password)
        driver.find_element('id', 'btnApply').click()

        driver.get(f"http://{ host }/GS116Ev2.cfg")

        # wait for the download
        seconds = 0
        while seconds <= timeout:
            time.sleep(1)
            finished = True
            for file in os.listdir(temp_path):
                if file.endswith(".crdownload"):
                    finished = False
            if finished:
                break
            seconds += 1
