from selenium.webdriver.common.by import By


class BaseLocator:
    CATEGORY_LOCATORS = {
        "Laptops & Computers": (By.XPATH, "//a[contains(@href,'trending-deals-laptops-computers')]"),
        # "PC Gaming": (By.XPATH, "//a[contains(@href,'trending-deals-pc-gaming')]")
    }