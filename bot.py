import os
import random
import time
import json

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from db import *

load_dotenv()  # take environment variables from example_for_dot_env.


class Bot:
    def __init__(self):
        geckodriver_path = os.getenv('GECKODRIVER_PATH')
        firefox_binary = os.getenv('FIREFOX_BIN')
        self.driver = webdriver.Firefox(executable_path=geckodriver_path,
                                        firefox_binary=firefox_binary)

        self.driver.maximize_window()
        self.wait10 = WebDriverWait(self.driver, 10)
        self.wait30 = WebDriverWait(self.driver, 30)
        self.wait120 = WebDriverWait(self.driver, 120)

    def is_logged_in(self):
        try:
            # Execute JavaScript to get token value from local storage
            script = "return localStorage.getItem('pr_mw_exclusive_tab_key');"
            value = self.driver.execute_script(script)
            value = json.loads(value)
            return value is not None
        except:
            return False

    def login(self):
        self.driver.get("https://messages.google.com/web/authentication")
        while not self.is_logged_in():
            time.sleep(1)

        return True

    def send_message(self, mobile_number, content):
        start_new_conv_selector = "a[href='/web/conversations/new']"
        mobile_number_input_selector = ".input"
        send_to_mobile_number_btn_selector = ".button.mdc-button.mat-mdc-button.mat-unthemed.mat-mdc-button-base"
        message_input_selector = "textarea"

        self.wait10.until(EC.presence_of_element_located((By.CSS_SELECTOR, start_new_conv_selector)))
        time.sleep(random.uniform(1, 2))  # sleep random time between 1 and 3 seconds
        self.driver.find_element(By.CSS_SELECTOR, start_new_conv_selector).click()

        self.wait10.until(EC.presence_of_element_located((By.CSS_SELECTOR, mobile_number_input_selector)))
        time.sleep(random.uniform(1, 2))  # sleep random time between 1 and 3 seconds
        self.driver.find_element(By.CSS_SELECTOR, mobile_number_input_selector).send_keys(mobile_number)

        self.wait10.until(EC.presence_of_element_located((By.CSS_SELECTOR, send_to_mobile_number_btn_selector)))
        time.sleep(random.uniform(1, 2))  # sleep random time between 1 and 3 seconds
        self.driver.find_element(By.CSS_SELECTOR, send_to_mobile_number_btn_selector).click()

        self.wait10.until(EC.presence_of_element_located((By.CSS_SELECTOR, message_input_selector)))
        time.sleep(random.uniform(1, 2))  # sleep random time between 1 and 3 seconds
        self.driver.find_element(By.CSS_SELECTOR, message_input_selector).send_keys(content)

        time.sleep(random.uniform(1, 2))  # sleep random time between 1 and 3 seconds
        self.driver.find_element(By.CSS_SELECTOR, message_input_selector).send_keys(Keys.ENTER)

        return True


