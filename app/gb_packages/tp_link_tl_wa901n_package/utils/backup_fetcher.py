import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from pathlib import Path

class BackupFetcher:
    @staticmethod
    def fetch_backup(temp_path: str, host: str, password: str, timeout=60):
        options = Options()
        prefs = {"download.default_directory": temp_path}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome("chromedriver", options=options)

        driver.get(f"http://{host}")
        time.sleep(2)
        driver.find_element("id", "pcPassword").send_keys(password)
        driver.find_element('id', "loginBtn").click()
        time.sleep(2)
        if len(driver.find_elements("id", "loginBtn")) > 0:
            raise Exception("Wrong login credentials!")
        driver.execute_script("location.href='config.bin';")

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
