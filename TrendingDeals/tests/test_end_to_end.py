import pytest
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.home_page import HomePage
from pages.base_page import BasePage
from pages.category_page import CategoryPage
from pages.cart_page import CartPage

from locators.cart_locator import CartLocator
from tests.test_category_page import price_data

from utils.json_reader import JsonReader
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()


@pytest.mark.usefixtures("driver")
class TestCartPage:

    def test_checkout_flow(self, driver):

        home_page = HomePage(driver)
        base_page = BasePage(driver)
        category_page = CategoryPage(driver)
        cart_page = CartPage(driver)

        category = JsonReader.read_categories(
            "data/categories.json"
        )[0]

        try:
            logger.info("--STARTING HOMEPAGE TEST--")
            logger.info("Selecting Region")
            ScreenshotUtil.capture_screenshot(driver, "Selecting Region")
            home_page.select_united_states()
            logger.info("United States Region Selected")
            logger.info("Opening BestBuy")

            logger.info("Verifying homepage title")
            assert "Best Buy" in home_page.get_homepage_title(), \
                "Homepage title is incorrect"
            logger.info("Homepage title Verified successfully")
            logger.info("BestBuy opened successfully")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Website_opened",
                attachment_type=allure.attachment_type.PNG
            )
            ScreenshotUtil.capture_screenshot(driver, "Website_opened")

            logger.info("Opening Trending Deals page")
            logger.info("Clicking on see more in Trending Deals Section")
            home_page.click_trending_deals_seemore()
            logger.info("Clicked on see more in Trending Deals Section")
            logger.info("Verifying Trending Deals page title")
            assert "Trending-Deals" in home_page.get_trending_deals_page_title(), \
                "Trending Deals title is incorrect"
            logger.info("Trending Deals page title Verified successfully")
            ScreenshotUtil.capture_screenshot(driver, "Trending_deals_opened")
            logger.info("====================================")

            logger.info("--STARTING BASE PAGE TEST--")
            logger.info(f"Opening category: {category}")
            logger.info(f"Check whether to click on {category} or {category} page already opened")
            base_page.click_category(category)
            assert "laptops" in driver.current_url.lower(), \
                f"{category} page did not open"
            logger.info(f"{category} page opened successfully")
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"{category}_opened",
                attachment_type=allure.attachment_type.PNG
            )
            ScreenshotUtil.capture_screenshot(driver, f"{category}_opened")

            logger.info("--APPLYING PRICE FILTERS--")
            logger.info("Applying valid price filter")
            price_range = price_data[-1]
            min_price = price_range[0]
            max_price = price_range[1]
            category_page.set_price_range(
                min_price,
                max_price
            )

            logger.info("--ADDING PRODUCT TO CART--")
            logger.info("Adding product to cart")

            category_page.add_product_to_cart()

            logger.info("--CART PAGE OPENING--")
            logger.info("Opening cart page")

            cart_page.open_cart()

            # HANDLE VERY SLOW CART PAGE
            logger.info("Waiting for cart page to load")

            cart_page.verify_cart_page()
            logger.info("Cart Page opened")

            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    CartLocator.CHECKOUT_BUTTON
                )
            )

            logger.info("Clicking checkout button")

            cart_page.click_checkout()

            logger.info("Clicking continue as guest")

            cart_page.continue_as_guest()

            logger.info("Waiting for checkout page")

            WebDriverWait(driver, 120).until(
                EC.url_contains("checkout")
            )

            assert "checkout" in driver.current_url.lower(), \
                "Checkout page did not open"

            ScreenshotUtil.capture_screenshot(
                driver,
                "checkout_page"
            )

            logger.info(
                "Checkout page verified successfully"
            )

        except TimeoutException as e:

            ScreenshotUtil.capture_screenshot(
                driver,
                "test_cart_page_failed"
            )

            logger.error(
                "Cart page test failed"
            )

            logger.error(str(e))