import os
import time

import config

from selenium.common.exceptions import (
    NoSuchElementException,
    JavascriptException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from wheels._base import BaseCasinoManager

START_URL = "https://www.grosvenorcasinos.com"
CASINO_URL = "https://www.grosvenorcasinos.com/games/grosvenor-victoria-roulette"


class GrosvenorcasinosCasinoManager(BaseCasinoManager):
    def run_casino(self):
        self.load_page(self.casino_url)

        try:
            join_button = self.driver.find_element_by_css_selector("button.load-table")
        except NoSuchElementException:
            self.logger.exception("Join button not found!")
            return

        try:
            join_button.click()
        except ElementClickInterceptedException:
            self.logger.exception("Error when click the button.")
            return

        return True

    def switch_to_down_frame(self):
        WebDriverWait(driver=self.driver, timeout=15).until(
            EC.visibility_of_element_located(locator=(By.ID, "game-overlay-iframe"))
        )

        self.driver.switch_to.frame(
            self.driver.find_element_by_id("game-overlay-iframe")
        )

        self.logger.info("Sleep 10s before switching frame!")
        time.sleep(10)

        self.driver.switch_to.frame(self.driver.find_element_by_id("playerFrame"))

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
            self.logger.error("Script path found!")
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
    manager = GrosvenorcasinosCasinoManager(
        script_path=config.CASINO_SCRIPT, casino_url=CASINO_URL
    )
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
