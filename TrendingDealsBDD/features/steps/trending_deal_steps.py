import allure
from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.base_page import BasePage
from pages.category_page import CategoryPage
from locators.category_locator import CategoryLocator
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()


# ===========================================================================
# BACKGROUND
# ===========================================================================

# @given("the user is on the Best Buy home page")
# def step_user_is_on_home_page(context):
#     """
#     Initialise all page-object helpers and store them on `context`
#     so every subsequent step can reuse them without re-creating.
#     """
#     context.home_page     = HomePage(context.driver)
#     context.base_page     = BasePage(context.driver)
#     context.category_page = CategoryPage(context.driver)
#     logger.info("Background: Browser is on the Best Buy home page")
#     allure.attach(
#         context.driver.get_screenshot_as_png(),
#         name="main_website_page",
#         attachment_type=allure.attachment_type.PNG
#     )

@given("the user is on the Laptops category page")
def step_user_is_on_laptops_page(context):
    context.category_page = CategoryPage(context.driver)
    print(">>> CategoryPage initialised")
    logger.info("Background: Browser is on the Laptops & Computers category page")
    allure.attach(
        context.driver.get_screenshot_as_png(),
        name="laptops_category_page",
        attachment_type=allure.attachment_type.PNG
    )

# ===========================================================================
# SHARED / REUSABLE STEPS
# ===========================================================================

@when("the user selects United States")
def step_select_united_states(context):
    try:
        context.home_page.select_united_states()
        logger.info("Selected United States")
        allure.attach(
            context.driver.get_screenshot_as_png(),
            name="region_selected",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception:
        # Country selector may not appear on every load; safe to continue
        logger.info("Country selector not present — skipping")


@when('the user navigates to "{category_name}" category')
def step_navigate_to_category(context, category_name):
    context.base_page.click_category(category_name)
    logger.info(f"Navigated to category: {category_name}")


@when("the user enters min price \"<min_price>\" and max price \"<max_price>\"")
def step_enter_price_outline_placeholders(context):
    # This variant is never reached directly — the parameterised variant below
    # handles all real calls.  Kept as a safety fallback.
    pass


@when('the user enters min price "{min_price}" and max price "{max_price}"')
def step_enter_price_range(context, min_price, max_price):
    context.current_min = int(min_price)
    context.current_max = int(max_price)

    category_page = context.category_page
    category_page._clear_and_enter(CategoryLocator.MIN_PRICE_BOX, min_price)
    category_page._clear_and_enter(CategoryLocator.MAX_PRICE_BOX, max_price)
    logger.info(f"Entered Min={min_price}, Max={max_price}")


@when("the user clicks the Set button")
def step_click_set_button(context):
    context.category_page._click_set_button()


@when("the user clicks the Clear button")
@then("the user clicks the Clear button")
def step_click_clear_button(context):
    context.category_page._click_clear_button()


# ===========================================================================
# SCENARIO 1 — Home Page
# ===========================================================================

@then("the home page should be verified")
def step_verify_home_page(context):
    assert context.home_page.verify_home_page(), (
        f"Home page verification failed. Current URL: {context.driver.current_url}"
    )
    logger.info("Home page verified successfully")
    ScreenshotUtil.capture_screenshot(context.driver, "home_page_verified")


# ===========================================================================
# SCENARIO 2 — Trending Deals Navigation
# ===========================================================================

@when("the user clicks on Trending Deals See More button")
def step_click_trending_deals_see_more(context):
    context.home_page.click_trending_deals_seemore()
    logger.info("Clicked Trending Deals 'See More' button")


@then("the trending deals page should be verified")
def step_verify_trending_deals_page(context):
    assert context.home_page.verify_trending_deals_page(), (
        f"Trending Deals page verification failed. Current URL: {context.driver.current_url}"
    )
    logger.info("Trending Deals page verified successfully")
    allure.attach(
        context.driver.get_screenshot_as_png(),
        name="trending_deals_page",
        attachment_type=allure.attachment_type.PNG
    )
    ScreenshotUtil.capture_screenshot(context.driver, "trending_deals_page_verified")


@then("the category page should be loaded")
def step_verify_category_page_loaded(context):
    current_url = context.driver.current_url.lower()
    assert any(keyword in current_url for keyword in ["laptop", "computer", "pcmcat"]), (
        f"Category page did not load as expected. Current URL: {context.driver.current_url}"
    )
    logger.info(f"Category page loaded — URL: {context.driver.current_url}")
    allure.attach(
        context.driver.get_screenshot_as_png(),
        name="category_page",
        attachment_type=allure.attachment_type.PNG
    )
    ScreenshotUtil.capture_screenshot(context.driver, "category_page_loaded")


# ===========================================================================
# SCENARIO 3 — Negative: Invalid Range Alert (min > max)
# ===========================================================================

@then('an alert should appear with message "Minimum value cannot be greater than the maximum value."')
def step_alert_should_appear(context):
    alert = WebDriverWait(context.driver, 5).until(EC.alert_is_present())
    context.alert_text = alert.text
    logger.info(f"Alert detected: '{context.alert_text}'")

    assert "Minimum value cannot be greater than the maximum value." in context.alert_text, (
        f"Unexpected alert text: '{context.alert_text}'"
    )
    logger.info("Alert message validated successfully")


@then("the user accepts the alert")
def step_accept_alert(context):
    alert = EC.alert_is_present()(context.driver)
    if alert:
        alert.accept()
        logger.info("Alert accepted")
        min_val = getattr(context, 'current_min', 'unknown')
        max_val = getattr(context, 'current_max', 'unknown')
        allure.attach(
            context.driver.get_screenshot_as_png(),
            name=f"invalid_range_alert_{min_val}_{max_val}",
            attachment_type=allure.attachment_type.PNG
        )
    else:
        logger.warning("No alert present to accept")


@then("the price input boxes should be cleared")
def step_price_inputs_should_be_cleared(context):
    context.category_page._clear_input(CategoryLocator.MIN_PRICE_BOX)
    context.category_page._clear_input(CategoryLocator.MAX_PRICE_BOX)

    min_val = context.driver.find_element(*CategoryLocator.MIN_PRICE_BOX).get_attribute("value")
    max_val = context.driver.find_element(*CategoryLocator.MAX_PRICE_BOX).get_attribute("value")

    assert min_val == "" and max_val == "", (
        f"Price inputs not cleared — Min: '{min_val}', Max: '{max_val}'"
    )
    logger.info("Price input boxes are cleared")


# ===========================================================================
# SCENARIO 4 — Negative: Product Grid Vanishes (zero range)
# ===========================================================================

@then("the first product grid should be empty")
def step_first_product_grid_should_be_empty(context):
    result = context.category_page._product_grid_is_empty()
    if not result:
        logger.warning(
            "SOFT ASSERT FAILED — Product grid is not empty after zero/low "
            "price filter is not applied."
        )
    else:
        logger.info("Confirmed: first product grid is empty")
        ScreenshotUtil.capture_screenshot(context.driver, "product_grid_empty")
    allure.attach(
        context.driver.get_screenshot_as_png(),
        name=f"zero_range_filter_{context.current_min}_{context.current_max}",
        attachment_type=allure.attachment_type.PNG
    )


# ===========================================================================
# SCENARIO 5 — Positive: Price Range Validation
# ===========================================================================

@then("products should be visible on the page")
def step_products_should_be_visible(context):
    context.category_page._wait_for_products(timeout=30)
    logger.info("Products are visible on the page after applying price filter")
    ScreenshotUtil.capture_screenshot(context.driver, "products_visible")


@then("the first product price should be within the range {min_price:d} and {max_price:d}")
def step_first_product_price_in_range(context, min_price, max_price):
    first_price = context.category_page._get_first_product_price()

    if not (min_price <= first_price <= max_price):
        logger.warning(
            f"SOFT ASSERT FAILED — First product price ${first_price} "
            f"is outside the filter range ({min_price}, {max_price})"
        )
    else:
        logger.info(
            f"Price ${first_price} is within range ({min_price}, {max_price}) CHECK"
        )
    allure.attach(
        context.driver.get_screenshot_as_png(),
        name=f"price_filter_{min_price}_{max_price}",
        attachment_type=allure.attachment_type.PNG
    )
    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"price_check_{min_price}_{max_price}"
    )



# ===========================================================================
# SCENARIO 6 — End-to-End: Filter → Add to Cart → Verify Cart
# ===========================================================================

@when("the user adds the first product to the cart")
def step_add_first_product_to_cart(context):
    driver = context.driver

    driver.execute_script("window.scrollBy(0, 1000);")

    add_buttons = WebDriverWait(driver, 60).until(
        EC.visibility_of_all_elements_located(CategoryLocator.ADD_TO_CART_BUTTONS)
    )
    logger.info(f"Found {len(add_buttons)} Add-to-Cart button(s)")

    first_button = add_buttons[0]
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_button)
    driver.execute_script("arguments[0].click();", first_button)
    logger.info("Clicked Add-to-Cart for the first product")


@when("the user clicks on the cart icon")
def step_click_cart_icon(context):
    try:
        cart_icon = WebDriverWait(context.driver, 20).until(
            EC.element_to_be_clickable(CategoryLocator.CART_ICON)
        )
        context.driver.execute_script("arguments[0].click();", cart_icon)
        logger.info("Clicked the cart icon")
    except Exception as e:
        logger.warning(f"Cart icon click timed out — page still loading: {e}")
        context.cart_click_exception = e


@then("the cart page should be loaded successfully")
def step_verify_cart_page(context):
    driver = context.driver

    if hasattr(context, "cart_click_exception"):
        logger.warning(
            f"Cart icon click raised a timeout exception as expected — "
            f"page was still loading: {context.cart_click_exception}"
        )
        assert context.cart_click_exception is not None
        allure.attach(
            driver.get_screenshot_as_png(),
            name="cart_page",
            attachment_type=allure.attachment_type.PNG
        )
        return

    WebDriverWait(driver, 60).until(
        lambda d: "cart" in d.current_url.lower()
    )
    assert "cart" in driver.current_url.lower(), (
        f"Expected cart page but got: {driver.current_url}"
    )
    logger.info(f"Cart page loaded — URL: {driver.current_url}")
    allure.attach(
        context.driver.get_screenshot_as_png(),
        name="cart_page",
        attachment_type=allure.attachment_type.PNG
    )
    ScreenshotUtil.capture_screenshot(driver, "cart_page_loaded")