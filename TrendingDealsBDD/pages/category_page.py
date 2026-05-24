import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from locators.category_locator import CategoryLocator
from utils.logger import LogGen

logger = LogGen.loggen()


class CategoryPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    # ------------------------------------------------------------------
    # PRIVATE HELPERS
    # ------------------------------------------------------------------

    def _clear_and_enter(self, locator, value):
        """Clear a price input box and type the given value."""
        box = self.wait.until(EC.visibility_of_element_located(locator))
        box.click()
        box.send_keys("\ue009a")  # Ctrl+A  — select all existing text
        box.send_keys("\ue017")  # Delete  — remove it
        box.clear()  # belt-and-braces clear
        box.send_keys(str(value))
        return box

    def _click_set_button(self):
        set_button = self.wait.until(
            EC.element_to_be_clickable(CategoryLocator.SET_PRICE_BUTTON)
        )
        set_button.click()
        logger.info("Clicked Set button")

    def _click_clear_button(self):
        """Click the price-filter Clear button and wait for inputs to empty."""
        clear_button = self.wait.until(
            EC.element_to_be_clickable(CategoryLocator.CLEAR_PRICE_BUTTON)
        )
        clear_button.click()
        logger.info("Clicked Clear button")
        # Wait until both input boxes are visibly empty
        WebDriverWait(self.driver, 10).until(
            lambda d: (
                    d.find_element(*CategoryLocator.MIN_PRICE_BOX).get_attribute("value") == ""
                    and
                    d.find_element(*CategoryLocator.MAX_PRICE_BOX).get_attribute("value") == ""
            )
        )
        logger.info("Price filter cleared — input boxes are empty")

    def _clear_input(self, locator):
        """Keyboard-level clear for a single input box."""
        box = self.wait.until(EC.visibility_of_element_located(locator))
        box.send_keys("\ue009a")  # Ctrl+A
        box.send_keys("\ue017")  # Delete
        box.clear()

    def _handle_invalid_range_alert(self, min_price, max_price):
        """
        Wait for the 'min > max' alert, assert its text, accept it,
        then clear both inputs so the next pair starts fresh.
        """
        try:
            alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert_text = alert.text
            logger.info(f"Alert detected: '{alert_text}'")

            assert "Minimum value cannot be greater than the maximum value." in alert_text, (
                f"Unexpected alert text for range ({min_price}, {max_price}): '{alert_text}'"
            )

            alert.accept()
            logger.info("Alert accepted")

            # Clear inputs so the next pair can be entered cleanly
            self._clear_input(CategoryLocator.MIN_PRICE_BOX)
            self._clear_input(CategoryLocator.MAX_PRICE_BOX)
            logger.info("Inputs cleared after invalid-range alert")

        except TimeoutException:
            raise AssertionError(
                f"Expected invalid-range alert for ({min_price}, {max_price}) "
                f"but no alert appeared."
            )

    def _product_grid_is_empty(self):
        """
        There are 3 parent divs sharing data-testid="product-grid", each
        normally containing 10 grid-child divs (30 total).

        After applying a zero/low filter only the FIRST parent loses its
        10 children; the other two are untouched (20 remain overall).

        XPath: (//div[@data-testid='product-grid'])[1]

        Return True when that first parent has exactly 0 grid-child elements.
        """
        try:
            # Wait for the first product-grid div to lose all grid-child children
            WebDriverWait(self.driver, 20).until(
                lambda d: len(
                    d.find_element(
                        By.XPATH, "(//div[@data-testid='product-grid'])[1]"
                    ).find_elements(By.CLASS_NAME, "grid-child")
                ) == 0
            )
            logger.info("First product-grid is empty")
            return True
        except Exception as e:
            logger.info(f"product-grid not empty or not found: {e}")
            return False

    def _wait_for_products(self, timeout=30):
        """Wait until at least one Add-to-Cart button is visible."""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(CategoryLocator.ADD_TO_CART_BUTTONS)
        )
        logger.info("Products are visible after filter")

    def _get_first_product_price(self):
        """
        Return the live price of the first product as a float.
        Targets the first grid-child price span directly — no manual
        price input needed, and no full list of prices is built.
        Locator: (//div[@class='grid-child'])[1]
                   //div[@data-testid='price-block-customer-price']
                   //span[@aria-hidden='true']
        """
        first_product_price_locator = (
            By.XPATH,
            "(//div[@class='grid-child'])[1]"
            "//div[@data-testid='price-block-customer-price']"
            "//span[@aria-hidden='true']"
        )
        price_element = self.wait.until(
            EC.visibility_of_element_located(first_product_price_locator)
        )
        raw = price_element.text.strip().replace("$", "").replace(",", "")
        price = float(raw)
        logger.info(f"First product price: ${price}")
        return price

    # ------------------------------------------------------------------
    # PUBLIC API — called by the test
    # ------------------------------------------------------------------

    def apply_price_filters(self, price_pairs: list):
        """
        Apply all price-filter pairs in the order supplied and run the
        appropriate assertions for each scenario.

        Expected CSV order (and what each pair tests):
          (500, 100)  → negative — min > max  → alert expected
          (100,   0)  → negative — min > max  → alert expected
          (  0,   0)  → negative — grid vanishes after filter
          (  0, 100)  → negative — grid vanishes after filter
          (100,1000)  → positive — first product price in range, then clear
          (500,2000)  → positive — first product price in range, add to cart

        :param price_pairs: ordered list of (min_price, max_price) int tuples
                            loaded from price_range.csv
        """

        # Classify each pair so the logic below is data-driven
        negative_invalid = []  # min > max  → expects alert
        negative_vanishing = []  # grid disappears after filter
        positive = []  # valid range → price check

        for (mn, mx) in price_pairs:
            if mn > mx:
                negative_invalid.append((mn, mx))
            elif mn == 0:
                negative_vanishing.append((mn, mx))
            else:
                positive.append((mn, mx))

        # ── 1. NEGATIVE — invalid range (min > max) ────────────────────

        for (min_p, max_p) in negative_invalid:
            logger.info(f"=== Negative invalid-range test: ({min_p}, {max_p}) ===")

            self._clear_and_enter(CategoryLocator.MIN_PRICE_BOX, min_p)
            self._clear_and_enter(CategoryLocator.MAX_PRICE_BOX, max_p)
            logger.info(f"Entered Min={min_p}, Max={max_p}")

            self._click_set_button()
            # Assert alert appears with correct text, then clears inputs
            self._handle_invalid_range_alert(min_p, max_p)

        # ── 2. NEGATIVE — product grid vanishes ────────────────────────

        for (min_p, max_p) in negative_vanishing:
            logger.info(f"=== Negative vanishing-grid test: ({min_p}, {max_p}) ===")

            self._clear_and_enter(CategoryLocator.MIN_PRICE_BOX, min_p)
            self._clear_and_enter(CategoryLocator.MAX_PRICE_BOX, max_p)
            logger.info(f"Entered Min={min_p}, Max={max_p}")

            self._click_set_button()

            # Wait for the DOM change to settle, then assert grid is empty
            WebDriverWait(self.driver, 10).until(
                lambda d: self._product_grid_is_empty()
            )
            assert self._product_grid_is_empty(), (
                f"Expected product grid to be empty for range ({min_p}, {max_p}) "
                f"but products are still displayed."
            )
            logger.info(f"Confirmed: product grid is empty for range ({min_p}, {max_p})")

            self._click_clear_button()

        # ── 3. POSITIVE — price-range validation ───────────────────────

        for idx, (min_p, max_p) in enumerate(positive):
            logger.info(f"=== Positive test: ({min_p}, {max_p}) ===")
            is_last_pair = (idx == len(positive) - 1)

            self._clear_and_enter(CategoryLocator.MIN_PRICE_BOX, min_p)
            self._clear_and_enter(CategoryLocator.MAX_PRICE_BOX, max_p)
            logger.info(f"Entered Min={min_p}, Max={max_p}")

            self._click_set_button()
            self._wait_for_products(timeout=30)

            # Soft assertion — log failure without stopping the run
            first_price = self._get_first_product_price()
            if not (min_p <= first_price <= max_p):
                logger.warning(
                    f"SOFT ASSERT FAILED — First product price ${first_price} "
                    f"is outside the filter range ({min_p}, {max_p})"
                )
                # If you have pytest-check installed, swap the block above for:
                # import pytest_check as check
                # check.between(first_price, min_p, max_p,
                #               msg=f"Price {first_price} not in ({min_p},{max_p})")
            else:
                logger.info(
                    f"Price ${first_price} is within range ({min_p}, {max_p}) ✓"
                )

            if not is_last_pair:
                # Clear filter before the next positive pair
                self._click_clear_button()

        # ── 4. ADD TO CART (runs after the last positive filter) ───────

        logger.info("=== Add to Cart flow ===")

        # Scroll down so buttons are in the viewport
        self.driver.execute_script("window.scrollBy(0, 1000);")

        add_buttons = WebDriverWait(self.driver, 60).until(
            EC.visibility_of_all_elements_located(CategoryLocator.ADD_TO_CART_BUTTONS)
        )
        logger.info(f"Found {len(add_buttons)} Add-to-Cart button(s)")

        first_button = add_buttons[0]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", first_button
        )
        self.driver.execute_script("arguments[0].click();", first_button)
        logger.info("Clicked Add-to-Cart for the first product")

        # Navigate to cart page
        cart_icon = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(CategoryLocator.CART_ICON)
        )
        cart_icon.click()
        logger.info("Clicked cart icon")

        # Wait for cart URL and full page load
        WebDriverWait(self.driver, 30).until(
            lambda d: "cart" in d.current_url.lower()
        )
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        assert "cart" in self.driver.current_url.lower(), (
            f"Expected to land on the cart page but current URL is: {self.driver.current_url}"
        )
        logger.info(f"Cart page loaded successfully — URL: {self.driver.current_url}")
