import os
import time

import config

from selenium.common.exceptions import (
    NoSuchElementException,
    JavascriptException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import create_logger
from wheels._base import BaseCasinoManager

logger = create_logger(__name__)

START_URL = "https://casino.mrgreen.com/en-GB/login"
CASINO_URL = "https://casino.mrgreen.com/en-US/game/play/real/grand-casino-roulette"

CREDENTIALS = {
    "email": config.MRGREEN_EMAIL,
    "password": config.MRGREEN_PASSWORD,
}


class MrGreenCasinoManager(BaseCasinoManager):
    def login_to_casino(self):
        WebDriverWait(driver=self.driver, timeout=20).until(
            EC.visibility_of_element_located(locator=(By.XPATH, "//div[@container]"))
        )

        email_input = self.driver.find_element_by_css_selector("#email")
        pass_input = self.driver.find_element_by_css_selector("#password")
        button = self.driver.find_element_by_css_selector('button[type="submit"]')

        email_input.send_keys(CREDENTIALS["email"])
        pass_input.send_keys(CREDENTIALS["password"])

        button.submit()

        time.sleep(10)

    def run_casino(self):
        self.load_page(self.casino_url)
        return True

    def switch_to_down_frame(self):
        WebDriverWait(driver=self.driver, timeout=15).until(
            EC.presence_of_element_located(
                locator=(By.CSS_SELECTOR, "iframe[allowfullscreen]")
            )
        )

        self.driver.switch_to.frame(
            self.driver.find_element_by_css_selector("iframe[allowfullscreen]")
        )

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


def main():
    logger.info("Start MrGreen Casino Manager!")
    manager = MrGreenCasinoManager(
        script_path=config.CASINO_SCRIPT, casino_url=CASINO_URL
    )
    try:
        manager.load_page(url=START_URL)
        manager.login_to_casino()
        manager.run_casino()
        manager.execute_script()
        manager.start_process()
    except KeyboardInterrupt:
        manager.close()


if __name__ == "__main__":
    main()
