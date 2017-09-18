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
from selenium.webdriver.chrome.options import Options
import os

def initialize():
    config_parser = read_cfg_file()
    timeout_interval = int(config_parser.get('test_parameters','timeout_interval_in_seconds'))
    browser = config_parser.get('test_parameters','browser')
    if browser == 'firefox':
        driver = webdriver.Firefox()
    if browser == 'chrome' :
        chromeOptions = Options()
        chromeOptions.add_argument("--start-maximized")
        chromedriver = 'C:\\Python27\\Scripts\\chromedriver.exe'
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver,chrome_options=chromeOptions)
    
    url = config_parser.get('connection', 'website_url')
    driver.get(url)
    wait = WebDriverWait(driver, timeout_interval)
    elem = wait.until(EC.presence_of_element_located((By.ID,"sizes618069")))
    print "we are here .."
    #elem = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[12]/div[2]/div[3]/div/div[2]/div[3]/div[6]/div[1]/div/div[1]/div[1]/div[3]/div[1]/div[2]/div[3]/div/div[2]/ul/li[3]/span")))
    elem = driver.find_element_by_xpath("/html/body/div[12]/div[2]/div[3]/div/div[2]/div[3]/div[6]/div[1]/div/div[1]/div[1]/div[3]/div[1]/div[2]/div[3]/div/div[2]/ul/li[3]/span")
    #elem = driver.find_element_by_name('j_username')
    elem.click()
    elem = driver.find_element_by_xpath("/html/body/div[12]/div[2]/div[3]/div/div[2]/div[3]/div[6]/div[1]/div/div[1]/div[1]/div[3]/div[1]/div[4]/button")
    elem.click()
    driver.switch_to_default_content()
    #elem = driver.find_element_by_id("m_atb_checkout")
    #elem.click()
    #elem.send_keys(Keys.CONTROL + 't')
    driver.get("http://www1.macys.com/bag/index.ognc?cm_sp=navigation-_-top_nav-_-bag")
    driver.switch_to_default_content()
    return driver


if __name__ == '__main__':
    initialize()