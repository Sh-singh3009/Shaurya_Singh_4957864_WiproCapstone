from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from locators.cart_locator import CartLocator
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()


class CartPage:

    def __init__(self, driver):
        self.driver = driver

    def open_cart(self):
        try:
            logger.info("Waiting for cart icon")

            # Wait for the icon to be interactive
            cart_icon = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(CategoryLocator.CART_ICON)
            )
            logger.info("Clicking cart icon")
            cart_icon.click()

            # Capture verification screenshot
            logger.info("Waiting for cart page response")
            ScreenshotUtil.capture_screenshot(self.driver, "cart_page_opened")

            WebDriverWait(self.driver, 40).until(
                lambda driver:
                "cart" in driver.current_url.lower()
            )

            logger.info("Cart page opened successfully")

            ScreenshotUtil.capture_screenshot(
                self.driver,
                "cart_page_opened"
            )

            return True


        except TimeoutException as e:
            logger.error(
                f"Cart page took too long to respond: {str(e)}"
            )

            ScreenshotUtil.capture_screenshot(
                self.driver,
                "cart_timeout_error"
            )
            return False
        except WebDriverException as e:
            logger.error(
                f"Browser/Driver issue while opening cart: {str(e)}"
            )

            try:
                ScreenshotUtil.capture_screenshot(
                    self.driver,
                    "cart_webdriver_error"
                )
            except Exception:
                logger.warning(
                    "Driver became unresponsive during screenshot capture"
                )
            return False

    def verify_cart_page(self):
        try:
            # Safely poll for the URL string transformation
            WebDriverWait(self.driver, 30).until(
                lambda driver: "cart" in driver.current_url.lower()
            )
            return True

        except (TimeoutException, WebDriverException) as e:
            logger.error(
                f"Timeout validation failure: URL did not change to 'cart'. Current URL is: {self.driver.current_url}")
            return False
    def click_checkout(self):
        checkout_button = WebDriverWait(
            self.driver,
            120
        ).until(
            EC.element_to_be_clickable(
                CartLocator.CHECKOUT_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            checkout_button
        )

        checkout_button.click()

        logger.info(
            "Checkout button clicked"
        )

    def continue_as_guest(self):
        guest_button = WebDriverWait(
            self.driver,
            120
        ).until(
            EC.element_to_be_clickable(
                CartLocator.CONTINUE_AS_GUEST_BUTTON
            )
        )

        guest_button.click()

        logger.info(
            "Continue as guest clicked"
        )

    # def increase_product_quantity(self, quantity):
    #
    #     logger.info(
    #         f"Updating product quantity to {quantity}"
    #     )
    #
    #     # WAIT FOR QUANTITY DROPDOWN
    #     quantity_dropdown = WebDriverWait(self.driver, 20).until(
    #         EC.element_to_be_clickable(
    #             CartLocator.QUANTITY_DROPDOWN
    #         )
    #     )
    #
    #     # SELECT QUANTITY
    #     select = Select(quantity_dropdown)
    #
    #     select.select_by_visible_text(str(quantity))
    #
    #     WebDriverWait(self.driver, 10).until(
    #         lambda d: Select(quantity_dropdown).first_selected_option.text.strip() == str(quantity)
    #     )
    #
    #     logger.info(
    #         f"Selected quantity: {quantity}"
    #     )
    #
    #     ScreenshotUtil.capture_screenshot(
    #         self.driver,
    #         f"quantity_updated_{quantity}"
    #     )
    #
    # def verify_quantity_updated(self, quantity):
    #
    #     quantity_dropdown = WebDriverWait(
    #         self.driver,
    #         20
    #     ).until(
    #         EC.visibility_of_element_located(
    #             CartLocator.QUANTITY_DROPDOWN
    #         )
    #     )
    #
    #     selected_value = Select(
    #         quantity_dropdown
    #     ).first_selected_option.text.strip()
    #
    #     logger.info(
    #         f"Currently selected quantity: "
    #         f"{selected_value}"
    #     )
    #
    #     return selected_value == str(quantity)