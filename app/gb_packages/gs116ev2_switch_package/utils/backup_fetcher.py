import time

from gb_module.utils.selenium_util import SeleniumUtil


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

    @staticmethod
    def restore_backup(path: str, host: str, password: str, switch_type: str,
                     login_input_id: str, login_button_id: str,
                     backup_endpoint: str, timeout=60, protocol="http"):
        driver = SeleniumUtil.get_options_with_download_path("/")

        print("load login page ...")
        base_url = f"{protocol}://{ host }"
        driver.get(f"{base_url}/login.htm")
        time.sleep(2)
        print("login ...")
        driver.find_element('id', login_input_id).send_keys(password)
        driver.find_element('id', login_button_id).click()
        time.sleep(2)
        driver.find_element('id', 'System_Maintenance').click()
        time.sleep(2)
        driver.find_element('name', 'lv6').click()
        time.sleep(2)
        print("switch frame ...")
        driver.switch_to.frame('maincontent')
        time.sleep(1)
        print("input path ...")
        driver.find_element('id', 'fileField').send_keys(path)
        time.sleep(1)
        print("switch back ...")
        driver.switch_to.default_content()
        time.sleep(1)
        print("apply ...")
        driver.find_element('id', 'btn_Apply').click()
        print("reset ...")
        time.sleep(5)

        # wait for the download
        #SeleniumUtil.wait_for_download(temp_path, timeout)
