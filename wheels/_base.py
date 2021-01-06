import time

import config

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from utils import create_logger


class BaseCasinoManager:
    """
    Base Manager class with general logic for wheels automation.
    """

    def __init__(self, script_path, casino_url):
        self.driver = self.init_webdriver()
        self.script_path = script_path
        self.casino_url = casino_url

        self.logger = create_logger(__name__)

    def load_page(self, url):
        """
        Move to specific `url` in browser.
        """
        self.logger.info("Loading page: `%s`", url)
        self.driver.get(url)

    def login_confirm(self):
        """
        Blocking function for any manual
        actions before start main logic.
        """
        input("Hit Enter here if you have summited the form: <Enter>")
        self.logger.info("Login successfully approved!")

    def switch_to_top_frame(self):
        """
        Switch iFrame to main screen.
        """
        self.driver.switch_to.default_content()

    def reload_page(self):
        """
        Refresh current page.
        It needs for session expiration management.
        """
        self.driver.refresh()

    def run_casino(self):
        raise NotImplemented()

    def check_session_expired(self):
        raise NotImplemented()

    def execute_script(self):
        raise NotImplemented()

    def start_process(self):
        """
        Run infinite loop for checking session expiration.

        If session expired this method should restart all logic
        for scraping numbers:
            - Reload the current page.
            - Open casino, wait for page loaded and switch frames.
            - Execute scraping JS script.
        """
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
        """
        Close current tab in browser and stop driver.
        """
        self.driver.close()
        self.driver.quit()

    @staticmethod
    def init_webdriver():
        """
        Initialize Chrome Webdriver for local using.
        It uses `WebDriver Manager` for managing version of the browsers.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        browser.maximize_window()
        return browser

    @staticmethod
    def init_remote_webdriver():
        """
        Initialize Remote Webdriver for using with Selenoid.
        """
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
