from pages.home_page import HomePage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()


class TestHomepage:
    def test_homepage(self, driver):
        logger.info("Starting Homepage Test")
        home_page = HomePage(driver)

        logger.info("Selecting United States region")
        ScreenshotUtil.capture_screenshot(driver, "US_region_selected")
        home_page.select_united_states()
        logger.info("United States region selected successfully")

        logger.info("Verifying homepage URL")
        assert home_page.verify_home_page(), \
            "BestBuy homepage did not open correctly"
        logger.info("Homepage URL Verified successfully")

        logger.info("Verifying homepage title")
        assert "Best Buy" in home_page.get_homepage_title(), \
            "Homepage title is incorrect"
        logger.info("Homepage title Verified successfully")
        ScreenshotUtil.capture_screenshot(driver, "Website_opened")
        logger.info("BestBuy opened successfully")


    def test_trending_deals_page(self, driver):
        logger.info("Starting Trending Deals Test")
        home_page = HomePage(driver)

        logger.info("Selecting United States region")
        home_page.select_united_states()
        logger.info("United States region selected successfully")

        try:
            logger.info("Clicking Trending Deals See More")
            driver.implicitly_wait(5)
            home_page.click_trending_deals_seemore()
            logger.info("Successfully clicked on Trending Deals See more")
        except Exception as e:
            logger.error(f"Trending Deals page did not open: {e}")


        logger.info("Verifying Trending Deals page URL")
        assert home_page.verify_trending_deals_page(), \
            "Trending Deals page did not open"
        logger.info("Trending Deals page URL Verified successfully")

        logger.info("Verifying Trending Deals page title")
        assert "Trending-Deals" in home_page.get_trending_deals_page_title(), \
            "Trending Deals title is incorrect"
        logger.info("Trending Deals page title Verified successfully")


        logger.info("Trending Deals test passed successfully")
        logger.info("ALL HOMEPAGE TESTS PASSED SUCCESSFULLY")