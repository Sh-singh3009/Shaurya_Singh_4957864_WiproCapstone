import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.driver import get_driver

def before_all(context):
    print(">>> before_all called — launching browser")
    context.driver = get_driver()
    context.driver.get("https://www.bestbuy.com/")
    time.sleep(5)
    print(f">>> driver set: {context.driver}")

def after_all(context):
    context.driver.quit()