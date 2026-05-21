import pytest
from utils.driver import get_driver


@pytest.fixture(scope="module")
def driver():
    driver = get_driver()
    driver.get("https://www.bestbuy.com/")
    yield driver
    driver.quit()