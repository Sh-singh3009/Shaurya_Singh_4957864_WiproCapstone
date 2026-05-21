import time

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from locators.category_locator import CategoryLocator
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()


class CategoryPage:

    def __init__(self, driver):
        self.driver = driver

    def set_price_range(self, min_price, max_price):

        logger.info(f"Applying price filter Min:{min_price} Max:{max_price}")

        wait = WebDriverWait(self.driver, 20)

        min_box = wait.until(
            EC.visibility_of_element_located(
                CategoryLocator.MIN_PRICE_BOX
            ))

        max_box = wait.until(
            EC.visibility_of_element_located(
                CategoryLocator.MAX_PRICE_BOX
            ))

        min_box.clear()
        max_box.clear()

        min_box.send_keys(min_price)
        max_box.send_keys(max_price)

        logger.info(f"Min Price:{min_price} and Max Price:{max_price} entered successfully")

        ScreenshotUtil.capture_screenshot(self.driver,f"price_filter_{min_price}_{max_price}")
        set_button = wait.until(
            EC.element_to_be_clickable(
                CategoryLocator.SET_PRICE_BUTTON
            ))
        logger.info("Clicking set price button")
        # CLICK ONLY ONCE
        set_button.click()

        logger.info("Clicked on Set button")

        # INVALID RANGE TEST

        if int(min_price) > int(max_price):

            try:
                alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())

                logger.info(f"Alert message: {alert.text}")

                assert ("Minimum value cannot be greater than the maximum value." in alert.text)

                alert.accept()

                logger.info("Invalid range alert handled successfully")

                return "invalid_range"

            except TimeoutException:
                raise AssertionError("Expected alert did not appear")

        # ZERO RANGE TEST

        elif int(min_price) == 0 and int(max_price) == 0:

            products = self.driver.find_elements(*CategoryLocator.ADD_TO_CART_BUTTONS)

            logger.info(f"Products found for 0-0 range: {len(products)}")

            assert len(products) == 0, \
                "Products are displayed for 0-0 range"

            logger.info("No products displayed for 0-0 range")

            return "zero_range"

        # POSITIVE TEST

        else:

            wait.until(EC.url_contains("laptops-computers"))

            logger.info("Valid price filter applied successfully")

            return "positive_range"

    def add_product_to_cart(self):


        # WAIT FOR PAGE LOAD
        WebDriverWait(self.driver, 60).until(
            lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        # SCROLL DOWN
        self.driver.execute_script(
            "window.scrollBy(0, 1000);"
        )

        # WAIT FOR BUTTONS
        add_buttons = WebDriverWait(self.driver, 60).until(
            EC.visibility_of_all_elements_located(
                CategoryLocator.ADD_TO_CART_BUTTONS
            ))

        logger.info(f"Found {len(add_buttons)} add to cart buttons")

        # CLICK FIRST BUTTON
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_buttons[0]
        )

        time.sleep(2)
        logger.info("Clicking on Add to cart button")

        self.driver.execute_script(
            "arguments[0].click();",
            add_buttons[0]
        )
        logger.info("Clicked on Add to cart button")
        logger.info("Product added successfully")

        ScreenshotUtil.capture_screenshot(self.driver,"product_added")


    # def open_cart(self):
    #
    #     cart_icon = WebDriverWait(self.driver, 20).until(
    #         EC.element_to_be_clickable(
    #             CategoryLocator.CART_ICON
    #         )
    #     )
    #
    #     cart_icon.click()
    #
    #     ScreenshotUtil.capture_screenshot(
    #         self.driver,
    #         "cart_page_opened"
    #     )
    #
    #     logger.info("Cart page opened")
    #
    # def verify_cart_page(self):
    #
    #     WebDriverWait(self.driver, 30).until(
    #         lambda driver: "cart" in driver.current_url.lower()
    #     )
    #
    #     return "cart" in self.driver.current_url.lower()