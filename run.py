import os
import time

import config

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    JavascriptException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from utils import create_logger

logger = create_logger(__name__)

START_URL = "https://www.grosvenorcasinos.com"
CASINO_URL = "https://www.grosvenorcasinos.com/games/grosvenor-victoria-roulette"


class CasinoManager:
    def __init__(self, script_path, casino_url):
        self.driver = self.init_webdriver()
        self.script_path = script_path
        self.casino_url = casino_url

    @staticmethod
    def init_webdriver():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        browser = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            chrome_options=chrome_options,
        )
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
        logger.info("Loading page: `%s`", url)
        self.driver.get(url)

    @staticmethod
    def login_confirm():
        input("Hit Enter here if you have summited the form: <Enter>")
        logger.info("Login successfully approved!")

    def run_casino(self):
        self.load_page(self.casino_url)

        try:
            join_button = self.driver.find_element_by_css_selector("button.load-table")
        except NoSuchElementException:
            logger.exception("Join button not found!")
            return

        try:
            join_button.click()
        except ElementClickInterceptedException:
            logger.exception("Error when click the button.")
            return

        return True

    def switch_to_down_frame(self):
        WebDriverWait(driver=self.driver, timeout=15).until(
            EC.visibility_of_element_located(locator=(By.ID, "game-overlay-iframe"))
        )

        self.driver.switch_to.frame(
            self.driver.find_element_by_id("game-overlay-iframe")
        )

        logger.info("Sleep 10s before switching frame!")
        time.sleep(10)

        self.driver.switch_to.frame(self.driver.find_element_by_id("playerFrame"))

    def switch_to_top_frame(self):
        self.driver.switch_to.default_content()

    def reload_page(self):
        self.driver.refresh()

    def check_session_expired(self):
        self.switch_to_top_frame()
        self.switch_to_down_frame()

        try:
            self.driver.find_element_by_css_selector(
                css_selector='div[class*="titleContainer--"]'
            )
            return True
        except NoSuchElementException:
            return False

    def execute_script(self):
        if not os.path.exists(path=self.script_path):
            logger.error("Script path found!")
            return

        self.switch_to_top_frame()
        self.switch_to_down_frame()

        WebDriverWait(driver=self.driver, timeout=15).until(
            EC.visibility_of_element_located(
                locator=(By.CSS_SELECTOR, 'div[class*="statisticsBranding_triangle"]')
            )
        )

        casino_script = open(self.script_path).read()

        try:
            self.driver.execute_script(script=casino_script)
        except JavascriptException:
            pass

    def start_process(self):
        while True:
            if self.check_session_expired():
                logger.info("Session expired. Reload page!")
                self.reload_page()
                success = self.run_casino()

                if not success:
                    continue

                self.execute_script()

            logger.info("Sleep 10 sec before check session expired!")
            time.sleep(10)

    def close(self):
        self.driver.close()
        self.driver.quit()


def main():
    logger.info("Start Casino Manager!")
    manager = CasinoManager(script_path=config.CASINO_SCRIPT, casino_url=CASINO_URL)
    try:
        manager.load_page(url=START_URL)
        manager.login_confirm()
        manager.run_casino()
        manager.execute_script()
        manager.start_process()
    except KeyboardInterrupt:
        manager.close()


if __name__ == "__main__":
    main()
