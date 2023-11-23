import os
import random
import time
import json
import platform
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from db import *

load_dotenv()  # take environment variables from example_for_dot_env.


class Messanger:
    def __init__(self, make_sms_chat_failed=False, timeout_waiting=7):
        self.make_sms_chat_failed = make_sms_chat_failed  # if True, make all msg status sent in SMS chat failed
        self.timeout_waiting = timeout_waiting  # timeout waiting for msg status to be sent

        if platform.system() == "Linux":
            self.driver = webdriver.Firefox()
        elif platform.system() == "Windows":
            geckodriver_path = os.getenv('GECKODRIVER_PATH')
            firefox_binary = os.getenv('FIREFOX_BIN')

            self.driver = webdriver.Firefox(executable_path=geckodriver_path,
                                            firefox_binary=firefox_binary)

        self.driver.maximize_window()
        self.wait5 = WebDriverWait(self.driver, 5)
        self.wait10 = WebDriverWait(self.driver, 10)
        self.wait30 = WebDriverWait(self.driver, 20)
        self.wait120 = WebDriverWait(self.driver, 120)

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass

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
        try:
            self.driver.get("https://messages.google.com/web/authentication")
            while not self.is_logged_in():
                time.sleep(0.5)
            return True
        except:
            return False

    def send_message(self, mobile_number, content):
        try:

            # click on start new conversation on the left, enter mobile number,
            # click on send to <mobile_num>, enter message, click enter

            start_new_conv_selector = "a[href='/web/conversations/new']"
            mobile_number_input_selector = ".input"
            send_to_mobile_number_btn_selector = ".button.mdc-button.mat-mdc-button.mat-unthemed.mat-mdc-button-base"
            message_input_selector = "textarea"

            self.wait5.until(EC.presence_of_element_located((By.CSS_SELECTOR, start_new_conv_selector)))
            time.sleep(random.uniform(0, 0.2))  # sleep random time between 1 and 3 seconds
            self.driver.find_element(By.CSS_SELECTOR, start_new_conv_selector).click()

            self.wait5.until(EC.presence_of_element_located((By.CSS_SELECTOR, mobile_number_input_selector)))
            time.sleep(random.uniform(0, 0.2))  # sleep random time between 1 and 3 seconds
            self.driver.find_element(By.CSS_SELECTOR, mobile_number_input_selector).send_keys(mobile_number)

            self.wait5.until(EC.presence_of_element_located((By.CSS_SELECTOR, send_to_mobile_number_btn_selector)))
            time.sleep(random.uniform(0, 0.2))  # sleep random time between 1 and 3 seconds
            self.driver.find_element(By.CSS_SELECTOR, send_to_mobile_number_btn_selector).click()

            self.wait5.until(EC.presence_of_element_located((By.CSS_SELECTOR, message_input_selector)))
            time.sleep(random.uniform(0, 0.2))  # sleep random time between 1 and 3 seconds
            self.driver.find_element(By.CSS_SELECTOR, message_input_selector).send_keys(content)

            time.sleep(random.uniform(0, 0.1))  # sleep random time between 1 and 3 seconds
            self.driver.find_element(By.CSS_SELECTOR, message_input_selector).send_keys(Keys.ENTER)

            # wait until timestamp is visible and return status
            return self.__wait_and_get_msg_status()

        except:
            return "failed"

    def __wait_and_get_msg_status(self):  # wait until timestamp is visible and return status
        # self.wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-icon")))  # failed msg
        # self.wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".sent-icon")))  # sent msg in RCS chat only
        # self.wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".delivered-icon")))  # delivered msg in RCS chat only
        # self.wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".read-icon")))  # seen msg in RCS chat only
        try:
            # wait until sending icon to be invisible
            WebDriverWait(self.driver, self.timeout_waiting).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".sending-icon")))  # sending icon
            try:
                # if msg time stamp is appeared
                # either in RCS chat or SMS chat then msg is sent successfully
                # self.driver.find_element(By.CSS_SELECTOR, "mws-absolute-timestamp")

                # if msg is sent in RCS chat only then msg is sent successfully
                sent = delivered = read = None
                try:
                    self.driver.find_element(By.CSS_SELECTOR, ".sent-icon")
                    sent = True
                except:
                    sent = False
                try:
                    self.driver.find_element(By.CSS_SELECTOR, ".delivered-icon")
                    delivered = True
                except:
                    delivered = False
                try:
                    self.driver.find_element(By.CSS_SELECTOR, ".read-icon")
                    read = True
                except:
                    read = False

                if sent or delivered or read:
                    # print("sent")
                    return "sent"
                else:
                    # print("failed")
                    return "failed"

            except:
                # self.driver.find_element(By.CSS_SELECTOR, ".error-icon")
                # print("failed")
                return "failed"
        except:
            # print("timeout")
            return "timeout"
