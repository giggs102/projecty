'''
Created on Aug 22, 2015

@author: dsingh
'''

from login_setup import initialize
from main_engine import try_coupon_code


if __name__ == '__main__':
    
    driver = initialize()
    try_coupon_code(driver, "TESTCODE")