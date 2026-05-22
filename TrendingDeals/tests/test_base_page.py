import pytest
import allure

from pages.home_page import HomePage
from pages.base_page import BasePage
from utils.json_reader import JsonReader
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()


class TestTrendingDealsCategories:

    @pytest.mark.parametrize("category", JsonReader.read_categories("data/categories.json"))
    def test_select_trending_deals_category(self, driver, category):
        logger.info("Starting Test")
        home_page = HomePage(driver)
        base_page = BasePage(driver)

        logger.info("Selecting United States region")
        ScreenshotUtil.capture_screenshot(driver, "Selecting_US_region")
        home_page.select_united_states()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="BestBuy_opened",
            attachment_type=allure.attachment_type.PNG
        )
        ScreenshotUtil.capture_screenshot(driver, "BestBuy_opened")
        logger.info("United States region selected successfully")

        try:
            logger.info("Clicking Trending Deals See More")
            driver.implicitly_wait(10)
            home_page.click_trending_deals_seemore()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Trending_deals_opened",
                attachment_type=allure.attachment_type.PNG
            )
            ScreenshotUtil.capture_screenshot(driver, "Trending_deals_opened")
            logger.info("Successfully clicked on Trending Deals See more")
        except Exception as e:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Trending_deals_failed",
                attachment_type=allure.attachment_type.PNG
            )
            ScreenshotUtil.capture_screenshot(driver, "Trending_deals_failed")
            logger.error(f"Trending Deals page did not open: {e}")

        ScreenshotUtil.capture_screenshot(driver, f"clicking_on_{category}")
        logger.info(f"Clicking on {category} category")
        base_page.click_category(category)
        logger.info(f"{category} category clicked successfully")


        # Convert category into URL format
        expected_url_text = (
            category.lower()
            .replace(" & ", "-")
            .replace(" ", "-")
        )

        # Verify correct category page opened
        assert expected_url_text in driver.current_url.lower(), \
            f"{category} page did not open"
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"{category}_opened",
            attachment_type=allure.attachment_type.PNG
        )
        ScreenshotUtil.capture_screenshot(driver, f"{category}_opened")
        logger.info(f"{category} page opened successfully")
        logger.info("ALL BASE PAGE TESTS PASSED")