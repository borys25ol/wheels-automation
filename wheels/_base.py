import time

import config

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from utils import create_logger


class BaseCasinoManager:
    def __init__(self, script_path, casino_url):
        self.driver = self.init_webdriver()
        self.script_path = script_path
        self.casino_url = casino_url

        self.logger = create_logger(__name__)

    @staticmethod
    def init_webdriver():
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        browser.maximize_window()
        return browser

    @staticmethod
    def init_remote_webdriver():
        chrome_options = webdriver.ChromeOptions()
        capabilities = {
            "acceptInsecureCerts": True,
            "enableVNC": True,
            "screenResolution": "1280x1024x24",
            "sessionTimeout": "600m",
        }

        browser = RemoteWebDriver(
            command_executor=config.SELENOID_HOST,
            options=chrome_options,
            desired_capabilities=capabilities,
            keep_alive=True,
        )
        return browser

    def load_page(self, url):
        self.logger.info("Loading page: `%s`", url)
        self.driver.get(url)

    def login_confirm(self):
        input("Hit Enter here if you have summited the form: <Enter>")
        self.logger.info("Login successfully approved!")

    def run_casino(self):
        raise NotImplemented()

    def switch_to_top_frame(self):
        self.driver.switch_to.default_content()

    def reload_page(self):
        self.driver.refresh()

    def check_session_expired(self):
        raise NotImplemented()

    def execute_script(self):
        raise NotImplemented()

    def start_process(self):
        while True:
            if self.check_session_expired():
                self.logger.info("Session expired. Reload page!")
                self.reload_page()
                success = self.run_casino()

                if not success:
                    continue

                self.execute_script()

            self.logger.info("Sleep 10 sec before check session expired!")
            time.sleep(10)

    def close(self):
        self.driver.close()
        self.driver.quit()
