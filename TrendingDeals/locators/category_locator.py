from selenium.webdriver.common.by import By


class CategoryLocator:
    MIN_PRICE_BOX = (By.XPATH, "(//input[@placeholder='Min Price'])[3]")
    MAX_PRICE_BOX = (By.XPATH, "(//input[@placeholder='Max Price'])[3]")
    SET_PRICE_BUTTON = (By.XPATH, "(//span[text()='Set'])[3]")
    ADD_TO_CART_BUTTONS = (By.XPATH, "(//span[text()='Add to cart'])[30]")
    CART_ICON = (By.XPATH, "//span[text()='Cart']")