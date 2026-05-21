from selenium.webdriver.common.by import By


class CartLocator:

    QUANTITY_DROPDOWN = (By.XPATH, "//div[contains(@class,'tb-select-wrapper')]//select")
    CHECKOUT_BUTTON = (
        By.XPATH,
        "//button[text()='Checkout']"
    )

    CONTINUE_AS_GUEST_BUTTON = (
        By.XPATH,
        "//button[text()='Continue as Guest']"
    )