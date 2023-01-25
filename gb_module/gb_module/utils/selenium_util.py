from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

class SeleniumUtil:
    @staticmethod
    def get_options_with_download_path(temp_path: str, headless=True):
        options = Options()
        prefs = {"download.default_directory": temp_path}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome("chromedriver", options=options)
        # delete all cookies, because this driver is shared sometimes
        driver.delete_all_cookies()
        return driver

    @staticmethod
    def wait_for_download(temp_path: str, timeout=90):
        seconds = 0
        while seconds <= timeout:
            time.sleep(1)
            finished = True
            listdir = os.listdir(temp_path)
            if len(listdir) == 0:
                break
            for file in listdir:
                if file.endswith(".crdownload"):
                    finished = False
            if finished:
                break
            seconds += 1
