import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from pathlib import Path

from gb_module.gb_module.utils.selenium_util import SeleniumUtil


class BackupFetcher:
    @staticmethod
    def fetch_backup(temp_path: str, host: str, password: str, timeout=60):
        # fetch options
        driver = SeleniumUtil.get_options_with_download_path(temp_path)

        driver.get(f"http://{host}")
        time.sleep(2)
        driver.find_element("id", "pcPassword").send_keys(password)
        driver.find_element('id', "loginBtn").click()
        time.sleep(2)
        if len(driver.find_elements("id", "loginBtn")) > 0:
            raise Exception("Wrong login credentials!")
        driver.execute_script("location.href='config.bin';")

        # wait for the download
        SeleniumUtil.wait_for_download(temp_path, timeout)
