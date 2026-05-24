import sys
import os
import time
import allure
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.driver import get_driver

def before_all(context):
    print(">>> before_all called — launching browser")
    context.driver = get_driver()
    context.driver.get("https://www.bestbuy.com/")
    print(f">>> driver set: {context.driver}")

def after_scenario(context, scenario):
    log_file = "logs/automation.log"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log_content = f.read()
        allure.attach(
            log_content,
            name=f"logs_{scenario.name}",
            attachment_type=allure.attachment_type.TEXT
        )

def after_all(context):
    context.driver.quit()