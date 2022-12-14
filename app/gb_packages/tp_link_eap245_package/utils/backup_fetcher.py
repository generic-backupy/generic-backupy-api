import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from pathlib import Path

class BackupFetcher:
    @staticmethod
    def fetch_backup(temp_path: str, host: str, username: str, password: str, timeout=60):
        options = Options()
        prefs = {"download.default_directory": temp_path}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome("chromedriver", options=options)
        max_login_attempts = 20
        login_attempts = 0
        
        driver.get(f"http://{ host }")
        time.sleep(2)
        while login_attempts < max_login_attempts:
            driver.find_element(By.ID, "login-username").send_keys(username)
            driver.find_element(By.CSS_SELECTOR, "input[type=password]").send_keys(password)
            driver.find_element('id', "login-btn").click()
            time.sleep(2)
            if len(driver.find_elements('id', "login_btn")) == 0:
                break
            login_attempts += 1
            if login_attempts >= max_login_attempts:
                raise Exception("wrong credentials!")
        time.sleep(2)
        seconds = 0
        while seconds <= timeout:
            if len(driver.find_elements('id', "menu-top-system-tools-li")) == 0:
                driver.save_screenshot(Path(temp_path).joinpath(f'{seconds}_search_menu_thing.png'))
                time.sleep(1)
                seconds += 1
                continue
            driver.find_element('id', "menu-top-system-tools-li").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "a[name=backuprestore]").click()
            time.sleep(1)
            driver.find_element('id', "backup").click()
        time.sleep(2)

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
