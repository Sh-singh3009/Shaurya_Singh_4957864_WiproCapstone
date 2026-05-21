from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.home_locator import HomeLocator


class HomePage:
    def __init__(self, driver):
        self.driver = driver


    def select_united_states(self):
        us_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(HomeLocator.UNITED_STATES_BUTTON))
        us_button.click()


    def get_homepage_title(self):
        return self.driver.title


    def get_homepage_url(self):
        return self.driver.current_url


    def verify_home_page(self):
        return "bestbuy.com" in self.driver.current_url.lower()

    def click_trending_deals_seemore(self):
        self.driver.execute_script("window.scrollBy(0,700)")

        trending_deals = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                HomeLocator.TRENDING_DEALS_BUTTON))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", trending_deals)

        self.driver.execute_script(
            "arguments[0].click();", trending_deals)


    def get_trending_deals_page_title(self):
        return self.driver.title


    def get_trending_deals_page_url(self):
        return self.driver.current_url


    def verify_trending_deals_page(self):
        return "trending" in self.driver.current_url.lower()