<div align="center">

# 🛒 Best Buy Automation — Selenium Testing Framework

**Capstone Project | Wipro | E-Commerce Automation**

[![Python](https://img.shields.io/badge/Python-3.12.2-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/PyTest-Framework-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![BDD](https://img.shields.io/badge/BDD-Behave-5C4EE5?style=for-the-badge&logo=cucumber&logoColor=white)](https://behave.readthedocs.io/)
[![Allure](https://img.shields.io/badge/Allure-Reports-FF6B35?style=for-the-badge)](https://docs.qameta.io/allure/)


---

**Name:** Shaurya Singh &nbsp;|&nbsp; **Superset ID:** 4957864 &nbsp;|&nbsp; **Module:** Trending Deals

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Framework Architecture](#-framework-architecture)
- [Test Scenarios](#-test-scenarios)
- [Test Execution](#-test-execution)
- [Reports & Outputs](#-reports--outputs)
- [Results Summary](#-results-summary)

---

## 📌 Project Overview

This project automates the **Best Buy** web application using **Selenium WebDriver with Python**, covering the **Trending Deals** module on the Best Buy e-commerce platform.

The framework validates:
- 💰 Price filter functionality (valid, invalid, and boundary ranges)
- 🛒 Product grid behaviour under different filter conditions
- 🔁 End-to-end cart workflow — from product discovery to cart confirmation

The project is implemented using **two frameworks** in parallel:

| Framework | Approach | Test Count |
|---|---|---|
| **Selenium PyTest** | Data-driven with JSON & CSV | 7 tests |
| **Selenium Behave BDD** | Gherkin Given-When-Then | 6 scenarios |

Both frameworks follow the **Page Object Model (POM)** design pattern and are integrated with **Allure Reports**, **Python logging**, and **screenshot capture utilities**.

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.12.2 |
| Browser Automation | Selenium WebDriver |
| Test Framework | PyTest + Behave BDD |
| BDD Syntax | Gherkin (Given / When / Then) |
| Design Pattern | Page Object Model (POM) |
| Reporting | Allure Reports |
| Logging | Python Logging Module |
| Screenshots | Custom Screenshot Utility |
| Test Data | JSON (categories) + CSV (price ranges) |
| IDE | PyCharm |
| Browser | Google Chrome |
| OS | Windows 11 |

---

## 📁 Project Structure

The repository contains two independent automation frameworks:

### Selenium PyTest Framework — `TrendingDeals/`

```
TrendingDeals/
├── data/
│   ├── categories.json           # Category names for data-driven navigation
│   └── price_range.csv           # Price filter pairs for parametrized tests
│
├── locators/
│   ├── home_locator.py
│   ├── base_locator.py
│   ├── category_locator.py
│   └── cart_locator.py
│
├── pages/
│   ├── home_page.py
│   ├── base_page.py
│   ├── category_page.py
│   └── cart_page.py
│
├── tests/
│   ├── test_home_page.py
│   ├── test_base_page.py
│   ├── test_category_page.py
│   └── test_end_to_end.py
│
├── utils/
├── screenshots/
├── reports/
│   ├── screenshots/
│   ├── results_category/
│   └── allure_report_category/
│
├── logs/
├── conftest.py
└── requirements.txt
```

### Selenium Behave BDD Framework — `TrendingDealsBDD/`

```
TrendingDealsBDD/
├── data/
│   └── price_range.csv
│
├── features/
│   ├── 01_price_filter.feature
│   ├── 02_end_to_end.feature
│   ├── environment.py
│   └── steps/
│       └── trending_deal_steps.py
│
├── locators/
│   ├── base_locator.py
│   ├── category_locator.py
│   └── home_locator.py
│
├── pages/
│   ├── base_page.py
│   ├── category_page.py
│   └── home_page.py
│
├── utils/
│   ├── csv_reader.py
│   ├── driver.py
│   ├── logger.py
│   └── screenshot_util.py
│
├── logs/
│   └── automation.log
├── allure-results/
├── allure-report/
├── conftest.py
└── requirements.txt
```

---

## 🏗 Framework Architecture

Both frameworks use the **Page Object Model (POM)** pattern:

```
Test Layer  ──▶  Page Layer  ──▶  Locator Layer  ──▶  Browser (Selenium WebDriver)
     │                │
  Test Data        Utilities
(JSON / CSV)   (Logger, Screenshots, Driver)
```

### Key Design Decisions

- **`conftest.py`** — manages the browser fixture with `scope="module"` so a single browser session is shared across all tests in the module
- **`CategoryPage`** — the core page object that handles all price filter logic: entering values, handling alerts, asserting grid state, validating prices, and adding to cart
- **Soft assertions** — used for price range validation and zero-range grid checks so the test run continues while logging failures
- **Data files** — `categories.json` drives category navigation; `price_range.csv` drives all filter pair scenarios

---

## ✅ Test Scenarios

### Selenium PyTest — 7 Test Cases

| # | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|
| 1 | Positive + E2E | Price Filter (500–2000) → Add to Cart → Verify Cart | User lands on cart page with product added | ✅ Passed |
| 2 | Positive | Category navigation from `categories.json` | User lands on correct category page | ✅ Passed |
| 3 | Positive | Price Range Validation (100–1000) | Products visible, first price within range | ✅ Passed |
| 4 | Negative | Invalid Range Alert (500, 100) | Alert shown: min > max message | ✅ Passed |
| 5 | Negative | Invalid Range Alert (100, 0) | Alert shown: min > max message | ✅ Passed |
| 6 | Negative | Zero Range Grid Vanishes (0, 0) | Product grid disappears after filter | ✅ Passed |
| 7 | Positive | Zero Range Filter (0, 100) | Products still displayed | ✅ Passed |

### Selenium Behave BDD — 6 Scenarios

| # | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|
| 1 | E2E + Positive | Filter (500–2000) → Add to Cart → Verify Cart | Cart page loads with product added | ✅ Passed |
| 2 | Positive | Price Range Validation (100–1000) | Products visible, first price within range | ✅ Passed |
| 3 | Negative | Invalid Range Alert (500, 100) | Alert displayed with invalid range message | ✅ Passed |
| 4 | Negative | Invalid Range Alert (100, 0) | Alert displayed with invalid range message | ✅ Passed |
| 5 | Negative | Zero Range Grid Vanishes (0, 0) | Product grid disappears after filter | ✅ Passed |
| 6 | Negative | Zero Range Grid Vanishes (0, 100) | Product grid disappears after filter | ✅ Passed |

---

## ▶ Test Execution

### Prerequisites

Install all dependencies:

```bash
pip install -r requirements.txt
```

**`requirements.txt` includes:**
```
selenium
pytest
webdriver-manager
allure-pytest
behave
allure-behave
pytest-bdd
pytest-check
```

---

### Running the PyTest Framework

```bash
# Run all tests
pytest tests/ -v

# Run with Allure reporting
pytest tests/ -v --alluredir=reports/allure-results

# Run a specific test file
pytest tests/test_category_page.py -v

# Run a specific test by name
pytest tests/ -v -k "price_filter"
```

### Running the BDD Framework

```bash
# Run all BDD scenarios
behave features/

# Run with Allure reporting
behave features/ -f allure_behave.formatter:AllureFormatter -o allure-results/

# Run a specific feature file
behave features/01_price_filter.feature
```

### Generating the Allure Report

```bash
# Serve report locally (auto-opens browser)
allure serve reports/allure-results

# Generate static report
allure generate reports/allure-results -o reports/allure-report --clean
```

---

## 📊 Reports & Outputs

### Screenshot Capture

The framework automatically captures screenshots at key execution stages:

| Stage | Screenshot |
|---|---|
| Website opening | Home page load |
| Trending Deals navigation | Category page load |
| Price filter applied | Filter with values entered |
| Add to Cart | Product add action |
| Cart page | Final cart verification |

Screenshots are saved to `reports/screenshots/` (PyTest) and captured inline in Allure reports for both frameworks.

### Allure Reports

Allure Reports are integrated with both frameworks and provide:
- ✅ Pass/fail status per test and scenario
- 📸 Screenshots at each key execution stage
- 📋 Step-by-step execution flow
- 🪵 Per-test log attachments for debugging
- 📈 Execution history and trend tracking

### Execution Logs

Detailed logs are generated using Python's logging framework and saved to `logs/automation.log`, covering every page action, assertion, and exception.

---

## 📈 Results Summary

### PyTest Framework

| Metric | Value |
|---|---|
| Total Tests Executed | 7 |
| Tests Passed | 7 |
| Tests Failed | 0 |
| Automation Accuracy | **100%** |

### Behave BDD Framework

| Metric | Value |
|---|---|
| Total Scenarios Executed | 6 |
| Scenarios Passed | 6 |
| Scenarios Failed | 0 |
| Automation Accuracy | **100%** |

---

## 🔍 Test Environment

| Property | Value |
|---|---|
| Operating System | Windows 11 |
| IDE | PyCharm |
| Browser | Google Chrome |
| Language | Python 3.12.2 |
| Design Pattern | Page Object Model (POM) |
| Reporting Tool | Allure Reports |

---

## 📝 Conclusion

The automation framework successfully validates the Best Buy Trending Deals module using both **Selenium PyTest** and **Selenium Behave BDD** approaches. All test cases and scenarios passed with **100% accuracy** across both frameworks.

The project demonstrates:
- 🏗 **Scalable architecture** using Page Object Model
- 🔄 **Data-driven testing** with JSON and CSV inputs
- 📖 **BDD readability** with Gherkin Given-When-Then structure
- 📊 **Professional reporting** with Allure integration
- 🛡 **Robust error handling** with soft assertions and alert management
- ♻️ **Reusable components** across both frameworks

---

<div align="center">

**Best Buy Automation | Selenium Testing Report**
Wipro Capstone Project · Shaurya Singh · 4957864

</div>
