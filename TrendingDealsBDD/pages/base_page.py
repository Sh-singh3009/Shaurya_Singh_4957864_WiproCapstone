from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.base_locator import BaseLocator
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()

class BasePage:
    def __init__(self, driver):
        self.driver = driver


    def click_category(self, category_name):
        expected_url = (
            category_name.lower()
            .replace(" & ", "-")
            .replace(" ", "-")
        )
        # If already on correct page, do nothing
        if expected_url in self.driver.current_url.lower():
            logger.info(f"{category_name} page already opened")
            ScreenshotUtil.capture_screenshot(self.driver, f"{category_name}_already_opened")
            return
        # Otherwise click category
        locator = BaseLocator.CATEGORY_LOCATORS[category_name]

        category = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(locator)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            category
        )
        category.click()
