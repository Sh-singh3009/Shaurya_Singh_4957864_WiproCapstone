Feature: Best Buy Price Filter and Add to Cart

#  Background:
#    Given the user is on the Best Buy home page
    Background:
      Given the user is on the Laptops category page

  # ---------------------------------------------------------------------------
  # Scenario 1 — Home Page
  # ---------------------------------------------------------------------------

#  Scenario: User lands on Best Buy home page and selects United States
#    When the user selects United States
#    Then the home page should be verified


  # ---------------------------------------------------------------------------
  # Scenario 2 — Category Navigation
  # ---------------------------------------------------------------------------

#  Scenario: User navigates to Laptops and Computers category
#    When the user selects United States
#    And the user clicks on Trending Deals See More button
#    Then the trending deals page should be verified
#    When the user navigates to "Laptops & Computers" category
#    Then the category page should be loaded


  # ---------------------------------------------------------------------------
  # Scenario 3 — Negative: Invalid Range Alert (min > max)
  # ---------------------------------------------------------------------------

  Scenario Outline: Invalid price range triggers an alert when min is greater than max
#    When the user selects United States
    When the user enters min price "<min_price>" and max price "<max_price>"
#    And the user navigates to "Laptops & Computers" category
#    And the user enters min price "<min_price>" and max price "<max_price>"
    And the user clicks the Set button
    Then an alert should appear with message "Minimum value cannot be greater than the maximum value."
    And the user accepts the alert
    And the price input boxes should be cleared

    Examples:
      | min_price | max_price |
      | 500       | 100       |
      | 100       | 0         |


  # ---------------------------------------------------------------------------
  # Scenario 4 — Negative: Product Grid Vanishes (zero range)
  # ---------------------------------------------------------------------------

  Scenario Outline: Zero price range causes product grid to disappear
#    When the user selects United States
    When the user enters min price "<min_price>" and max price "<max_price>"
#    And the user navigates to "Laptops & Computers" category
#    And the user enters min price "<min_price>" and max price "<max_price>"
    And the user clicks the Set button
    Then the first product grid should be empty
    And the user clicks the Clear button

    Examples:
      | min_price | max_price |
      | 0         | 0         |
      | 0         | 100       |


  # ---------------------------------------------------------------------------
  # Scenario 5 — Positive: Price Range Validation (100 to 1000)
  # ---------------------------------------------------------------------------

  Scenario: First product price is within the applied filter range of 100 to 1000
#    When the user selects United States
    When the user enters min price "100" and max price "1000"
#    And the user navigates to "Laptops & Computers" category
#    And the user enters min price "100" and max price "1000"
    And the user clicks the Set button
    Then products should be visible on the page
    And the first product price should be within the range 100 and 1000
    And the user clicks the Clear button


  # ---------------------------------------------------------------------------
  # Scenario 6 — End to End: Filter, Add to Cart, Verify Cart (500 to 2000)
  # ---------------------------------------------------------------------------

  Scenario: End to end — filter products, add first product to cart and verify cart page
#    When the user selects United States
#    And the user navigates to "Laptops & Computers" category
    When the user enters min price "500" and max price "2000"
#    And the user enters min price "500" and max price "2000"
#    And the user clicks the Set button
    Then products should be visible on the page
    And the first product price should be within the range 500 and 2000
    When the user adds the first product to the cart
    And the user clicks on the cart icon
    Then the cart page should be loaded successfully
