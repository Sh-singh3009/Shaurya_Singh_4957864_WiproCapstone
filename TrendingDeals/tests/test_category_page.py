import pytest
from pages.home_page import HomePage
from pages.base_page import BasePage
from pages.category_page import CategoryPage
from utils.json_reader import JsonReader
from utils.csv_reader import CSVReader
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()

price_data = [
    (row["min_price"], row["max_price"])
    for row in CSVReader.read_csv("price_range.csv")
]


@pytest.mark.usefixtures("driver")
class TestCategoryPage:

    @classmethod
    def setup_class(cls):
        cls.first_run = True

    @pytest.mark.parametrize("min_price,max_price", price_data)
    def test_add_products_to_cart(self, driver, min_price, max_price):
        home_page = HomePage(driver)
        base_page = BasePage(driver)
        category_page = CategoryPage(driver)

        category = JsonReader.read_categories(
            "data/categories.json"
        )[0]

        # OPEN PAGE ONLY FIRST TIME
        if TestCategoryPage.first_run:

            logger.info("Opening BestBuy Homepage")

            home_page.select_united_states()

            logger.info("Opening Trending Deals page")

            home_page.click_trending_deals_seemore()

            logger.info(f"Opening category: {category}")

            base_page.click_category(category)

            TestCategoryPage.first_run = False

        else:
            logger.info("Refreshing category page")

            driver.refresh()

        try:
            category_page.set_price_range(
                min_price,
                max_price
            )
            # ONLY FOR LAST POSITIVE TEST CASE
            if (
                    int(min_price) == 500
                    and int(max_price) == 2000
            ):
                logger.info(
                    "Executing add to cart flow "
                    "for final positive dataset"
                )

                category_page.add_product_to_cart()
                logger.info(f"Product added to cart for price range: {min_price} - {max_price}")
        except Exception as e:

            ScreenshotUtil.capture_screenshot(
                driver,
                "category_test_failed"
            )

            logger.error(
                f"Test failed for "
                f"Min:{min_price} Max:{max_price}"
            )

            logger.error(str(e))

            raise