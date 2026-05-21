from selenium.webdriver.common.by import By


class HomeLocator:
    UNITED_STATES_BUTTON = (By.LINK_TEXT,"United States")
    TRENDING_DEALS_BUTTON = (By.XPATH, "//a[contains(@href,'trending-deals')]")