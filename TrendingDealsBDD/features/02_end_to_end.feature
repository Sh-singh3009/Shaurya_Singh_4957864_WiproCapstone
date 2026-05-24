Feature: Best Buy End to End — Filter, Add to Cart and Verify Cart

  Background:
    Given the user is on the Laptops category page


  # ---------------------------------------------------------------------------
  # End to End: Filter → Add to Cart → Verify Cart (500 to 2000)
  # ---------------------------------------------------------------------------
  Scenario: End to end — filter products, add first product to cart and verify cart page
#    When the user selects United States
#    And the user navigates to "Laptops & Computers" category
    When the user enters min price "500" and max price "2000"
    And the user clicks the Set button
    Then products should be visible on the page
    And the first product price should be within the range 500 and 2000
    When the user adds the first product to the cart
    And the user clicks on the cart icon
    Then the cart page should be loaded successfully
