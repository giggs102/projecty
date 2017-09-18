'''
Created on Jun 11, 2015

@author: dsingh
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os.path
from datetime import datetime
import ConfigParser
import sys



def help_args():
    print "The program takes the following arguments :"
    print "In order to execute all test cases include 'all' in the command line arguments "
    print "usage : python default_reports_performance_test.py all"
    print "In order to execute custom test cases include the specific test case numbers or the range. You can include as many test case numbers or ranges as required seperated by space "
    print "usage : python default_reports_performance_test.py 3-8 14 18 30-39 \n"


def read_cfg_file():
    config_parser = ConfigParser.RawConfigParser()
    config_file_path = 'cfg.txt'
    config_parser.read(config_file_path)
    return config_parser

def get_multiple_frame_reports():
    config_parser = read_cfg_file()
    return config_parser.get('test_parameters','multiple_frame_reports').split(',')

def get_data_reports():
    config_parser = read_cfg_file()
    return config_parser.get('test_parameters','data_reports').split(',')

def initialize():
    config_parser = read_cfg_file()
    browser = config_parser.get('test_parameters','browser')
    if browser == 'firefox':
        driver = webdriver.Firefox()
    if browser == 'chrome' :
        driver = webdriver.Chrome('C:\Users\dsingh\Downloads\chromedriver.exe')
    
    url = config_parser.get('connection', 'default_report_url')
    username = config_parser.get('connection', 'username')
    password = config_parser.get('connection', 'password')
    driver.get(url)
    
    #elem = driver.find_element_by_name('j_username')
    elem = driver.find_element_by_name('username')
    elem.send_keys(username)
    
    #elem = driver.find_element_by_name('j_password')
    elem = driver.find_element_by_name('password')
    elem.send_keys(password)
    
    elem.send_keys(Keys.RETURN)
    
    
    #timeout_interval= float(config_parser.get('test_parameters','timeout_interval_in_seconds'))
    #wait = WebDriverWait(driver, timeout_interval)
    #wait.until(EC.presence_of_element_located((By.ID,'dropdownMenu1')))
    
    #elem.send_keys(Keys.CONTROL + 't')
    
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.get(url)
    driver.switch_to_default_content()
    return driver

def goto_mainpage(driver):
    config_parser = read_cfg_file()
    url = config_parser.get('connection', 'default_report_url')
    driver.get(url)
    driver.switch_to_default_content()
    return driver

def get_elements_by_class_name(driver,class_name):
    elem_list = driver.find_elements_by_class_name(class_name)
    return elem_list

def write_output_file(message):
    config_parser = read_cfg_file()
    if not os.path.exists('performance_results/'):
        os.makedirs('performance_results/')
    if (config_parser.get('files', 'custom_output_file_names') == 'True'):
        file_name =  'performance_results/' + config_parser.get('files', 'output_summary_file_name')
    else:
        now = datetime.now()
        file_name = 'performance_results/default_rep_performance_test-'+str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'.log'    
    if os.path.isfile(file_name):
        log_file = open(file_name,'a')
    else:
        log_file = open(file_name,'w')
        log_file.write("Default_Report_Name" + "\t" + "Report_URI" + "\t" + "Load Time (Seconds)" + '\t' + "Result" + '\n')
        
    log_file.write(message)
    log_file.close()
    

def save_screenshot(driver,report_name):
    if not os.path.exists('screenshots/'):
        os.makedirs('screenshots/')
    filename = 'screenshots/' + report_name.replace(' ','_') + '.png'
    driver.get_screenshot_as_file(filename)
    print "Screenshot saved : ",
    print filename

def write_to_log_file(msg):
    now = datetime.now()
    if not os.path.exists('logs/'):
        os.makedirs('logs/')
    file_name = 'logs/output-'+str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'.log'
    if os.path.isfile(file_name):
        log_file = open(file_name,'a')
    else:
        log_file = open(file_name,'w')
    log_file.write(msg)
    log_file.close()
    
def get_cmd_arguments():
    if sys.argv[1] == 'all':
        return 'all'
    else:
        tc_numbers = []
        for arg in sys.argv[1:]:
            if '-' in arg:
                arg_range = arg.split('-')
                for tc in list(range(int(arg_range[0]),int(arg_range[1])+1)):
                    tc_numbers.append(tc)
            else:
                tc_numbers.append(int(arg))
        return tc_numbers


def wait_for_elements_by_id(element_id_list,driver):
    config_parser = read_cfg_file()
    timeout_time = float(config_parser.get('test_parameters','timeout_interval_in_seconds'))
    time_elapsed = 0.0
    while True:
        for element_id in element_id_list:
            try:
                driver.find_element_by_id(element_id)
                return element_id
            except NoSuchElementException:
                pass
        time.sleep(0.2)
        time_elapsed += 0.2
        if time_elapsed > timeout_time:
            raise Exception('Timeout ...')

def detect_popup_dialog(xpath,driver):
    tested_xpath = False
    tested_dialog = False 
    config_parser = read_cfg_file()
    timeout_time = float(config_parser.get('test_parameters','timeout_interval_in_seconds'))
    time_elapsed = 0.0
    while True:
        try:
            if not tested_dialog: 
                tested_dialog = True
                tested_xpath = False
                driver.find_element_by_id('standardDialog')
                return('dialog_popup')
            if not tested_xpath:
                tested_xpath = True
                tested_dialog = False
                driver.find_element_by_xpath(xpath)
                try:
                    driver.find_element_by_class_name('noData')
                    return('no_data')
                except NoSuchElementException:
                    pass
                
                return('success')
        except NoSuchElementException:
            pass
        time.sleep(0.2)
        time_elapsed += 0.2
        if time_elapsed > timeout_time:
            raise Exception('Timeout ...')
        
            

    
def test_report(rep_name,driver):
    config_parser = read_cfg_file()
    
    driver = goto_mainpage(driver)
    timeout_interval = int(config_parser.get('test_parameters','timeout_interval_in_seconds'))
    wait = WebDriverWait(driver, timeout_interval)
    elem = wait.until(EC.presence_of_element_located((By.LINK_TEXT,rep_name)))
    time.sleep(1)
    print "Loading report : ",
    report_name = elem.text
    print report_name
    log_msg = "Loading report : " + report_name + '\n'
    start_time = time.time()
    elem.click()
    
    report_url = driver.current_url
    
    wait.until(EC.frame_to_be_available_and_switch_to_it("report-iframe"))
    
    element_id = wait_for_elements_by_id(['borderContainer','widget-area','contentArea'], driver)
    if element_id == 'borderContainer':
        report_type = 'single_frame'
    if element_id == 'widget-area':
        report_type = "multiple_frame"
    if element_id == 'contentArea':
        report_type =  'data_report'
        
       
    if report_type == "multiple_frame":
        print "Multiple frame report detected .."
        log_msg = log_msg + "Multiple frames report detected .." + "\n"
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"widgetContainer")))
        panels_list = driver.find_elements_by_class_name("widgetContainer")
        no_panels = len(panels_list)
        print 'No of Frames detected : ',
        print no_panels
        log_msg = log_msg + 'No of Frames detected : ' + str(no_panels) + '\n'
        i = 1
        res = 'success'
        while i <= no_panels :
            driver.switch_to_default_content()
            frame_name = "iframe_content-area-Panel_" + str(i)
            wait.until(EC.frame_to_be_available_and_switch_to_it('report-iframe'))
            wait.until(EC.frame_to_be_available_and_switch_to_it(frame_name))
            frame_res = detect_popup_dialog('/html/body/div[2]/div/div/div[7]/div', driver)
              
            print "Frame ",
            print str(i),
            print ' Loaded : ',
            print frame_res
            log_msg = log_msg + "Frame " + str(i) + ' Loaded : '+ frame_res + '\n'
            i+=1
            if frame_res == 'dialog_popup':
                res = frame_res
            if frame_res == 'no_data':
                res = frame_res
    
    elif report_type == 'data_report':
        print "Data Report detected.."
        log_msg = log_msg + "Data Report detected.." + '\n'
        
        res = detect_popup_dialog('/html/body/div[1]/div[4]/div[1]/div/table/tbody/tr[3]/td',driver)
        print res
        
    elif report_type == 'single_frame':
        print "Single frame report detected.."
        log_msg = log_msg + "Single frame report detected.." + '\n'
        res = detect_popup_dialog('/html/body/div[2]/div[5]/div[3]/div/div[7]/div',driver)
        print res
        
             
    time.sleep(0.2)
    load_time = str(time.time() - start_time)
    print "Loading report took : ",
    print load_time,
    print " seconds"
    save_screenshot(driver, report_name)
    log_msg = log_msg + "Loading report took : " + load_time + " seconds" + '\n' + "Screenshot saved : " + report_name.replace(' ','_') + '.png' + '\n\n'
    print '\n'
    
    output_message = report_name + '\t' + report_url + '\t' + load_time + '\t' + res +'\n'
    write_output_file(output_message)
    write_to_log_file(log_msg)
    time.sleep(3)
    

if __name__ == '__main__':
    
    driver = initialize()
    time.sleep(5)
    config_parser = read_cfg_file()
    timeout_interval = int(config_parser.get('test_parameters','timeout_interval_in_seconds'))
    wait = WebDriverWait(driver, timeout_interval)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"reports-item-title")))
    default_rep_list = get_elements_by_class_name(driver,"reports-item-title")
    default_rep_names = []
    for elem in default_rep_list:
        default_rep_names.append(elem.text)
    
    try:
        cmd_arguments = get_cmd_arguments()
    except Exception as e:
        print '\n'
        print e
        print '\n'
        help_args()
    
    test_case_numbers = []
    if isinstance(cmd_arguments,str):
        for tc in list(range(1,len(default_rep_names)+1)):
            test_case_numbers.append(tc)
    elif isinstance(test_case_numbers,list): 
        test_case_numbers = cmd_arguments
    
    report_number = 0
    print '\n'
    for rep_name in default_rep_names:
        try:
            report_number += 1
            if report_number in test_case_numbers:
                print 'Testing Report : ',
                print report_number
                test_report(rep_name,driver)
        except Exception as e:
            print e
            write_to_log_file("Error :" + '\n' + str(e))
            output_message = rep_name + '\t' + str(e).replace('\n','') +'\t'+'Timed_out' + '\n'
            write_output_file(output_message)
            try:
                save_screenshot(driver, rep_name)
            except Exception as e:
                print 'Error : ',
                print e
                print 'Unable to save Screenshot ..'
    driver.close()
    print "-- Test Completed --"