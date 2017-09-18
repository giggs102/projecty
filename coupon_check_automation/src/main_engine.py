'''
Created on Aug 22, 2015

@author: dsingh
'''

from commons import read_cfg_file
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def try_coupon_code(driver,coupon_code):
    config_parser = read_cfg_file()
    timeout_interval = int(config_parser.get('test_parameters','timeout_interval_in_seconds'))
    wait = WebDriverWait(driver, timeout_interval)
    promo_code_textbox = wait.until(EC.presence_of_element_located(By.ID,"promoCode"))
    promo_code_textbox.send_keys(coupon_code)
    promo_code_button = driver.find_element_by_id("applyPromoCode")
    promo_code_button.click()
    

    