import time

from gb_module.gb_module.utils.selenium_util import SeleniumUtil


class BackupFetcher:
    @staticmethod
    def fetch_backup(temp_path: str, host: str, password: str, switch_type: str,
                     login_input_id: str, login_button_id: str,
                     backup_endpoint: str, timeout=60, protocol="http"):
        driver = SeleniumUtil.get_options_with_download_path(temp_path)

        base_url = f"{protocol}://{ host }"
        driver.get(f"{base_url}/login.htm")
        time.sleep(2)
        driver.find_element('id', login_input_id).send_keys(password)
        driver.find_element('id', login_button_id).click()
        time.sleep(2)
        driver.get(f"{base_url}/{backup_endpoint}")

        # wait for the download
        SeleniumUtil.wait_for_download(temp_path, timeout)
