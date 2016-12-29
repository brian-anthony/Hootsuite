#!/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import sys
import os
import time

# Variables # Requires two arguments, the absolute path to the csv and the exact name of the social network
# Example # python hootsuite.py tweets.csv Tweeter_Account
USER = "username"
PASSWORD = "password"
CSV = str(sys.argv[1])
NETWORK = str(sys.argv[2])
LOG = '/tmp/report_hootsuite.txt'

def main():
    # Starting a PhantomJS window for HTTPS connections
    browser = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
    browser.set_window_size(1920, 1080)
    # Login to Hootsuite
    browser.get('http://hootesuite.com/login')
    username = browser.find_element_by_id("loginEmailInput")
    password = browser.find_element_by_id("loginPasswordInput")
    username.send_keys(USER)
    password.send_keys(PASSWORD)
    # Submit button always gets a "Click succeeded but Load Failed. Status: 'fail'" error # ?? #
    try:
	time.sleep(1)
	browser.find_element(By.XPATH, ".//*[@class='button _submit green']").click()
    except:
	time.sleep(10)
    # Close popup window
    browser.find_element(By.XPATH, ".//*[@class='ui-dialog-titlebar-close ui-corner-all icon-30 _close']").click()
    # Navigate to publisher and move away from menu
    browser.find_element(By.XPATH, ".//*[@class='icon-global-nav-19 x-publisher navIcon']").click()
    time.sleep(3)
    x = browser.find_element(By.XPATH, ".//*[@class='_viewBtn viewBtn _list btn-underline active']")
    hover = ActionChains(browser).move_to_element(x)
    hover.perform()
    time.sleep(1)
    # Open BulkUpload window
    browser.find_element(By.XPATH, ".//*[@class='tab _button _showBulkScheduleDialogBtn']").click()
    time.sleep(1)
    # Add the csv file
    x = os.path.abspath(CSV)
    browser.find_element_by_name("csvFile").send_keys(x)
    time.sleep(1)
    # Activate network select and pick a network
    browser.find_element(By.XPATH, ".//*[@class='btn-cmt _bulkScheduleBtn']").click()
    y = browser.find_element(By.XPATH, ".//*[@class='_defaultText defaultText']")
    hover = ActionChains(browser).move_to_element(y)
    hover.perform()
    time.sleep(1)
    browser.find_element(By.XPATH, ".//div[@class='stream-scroll _itemListBody']/div/div[@title='"+NETWORK+"']").click()
    # Submit
    browser.find_element(By.XPATH, ".//a[@class='btn-cmt _bulkScheduleBtn']").click()
    time.sleep(2)
    # Retrieve message, quit and report
    browser.switch_to.frame(browser.find_element(By.XPATH, ".//*[@id='scheduleFileUploadTarget']"))
    for elem in browser.find_elements(By.XPATH, ".//html"):
	z = 'Sucessfully uploaded '+CSV+' to '+NETWORK+' at '+time.strftime("%d/%m/%Y %H:%M:%S")+'\n'+elem.text
    # Logout and quit # Logout stalls sometimes. Why?
    #browser.find_element(By.XPATH, ".//span[@class='icon-global-nav-19 x-logout']").click()
    browser.quit()
    # How do we know if this is working or not?
    #z = 'Sucessfully uploaded '+CSV+' to '+NETWORK+' at '+time.strftime("%d/%m/%Y %H:%M:%S")
    with open(LOG, 'a') as file:
	file.write(z+'\n')

if __name__ == "__main__":
    # Check if CSV file actually exists.
    if not os.path.isfile(CSV):
	z = 'FAILED: '+time.strftime("%d/%m/%Y %H:%M:%S")+': "'+CSV+'" this csv file does not exist.'
	with open(LOG, 'a') as file:
	    file.write(z+'\n')
	sys.exit('Aborting because csv file could not be found.')
    # Check if CSV file is empty.
    elif not os.stat(CSV).st_size > 0:
	z = 'FAILED: '+time.strftime("%d/%m/%Y %H:%M:%S")+': "'+CSV+'" this csv file was empty.'
	with open(LOG, 'a') as file:
	    file.write(z+'\n')
	sys.exit('Aborting because csv file was empty.')
    else:
	try:
	    main()
	except Exception as e:
	    # Use "grep 'FAILED' report_hootsuite.txt" to see all failures. # Debugging this is going to be tough
	    z = 'FAILED: '+time.strftime("%d/%m/%Y %H:%M:%S")+': UNKNOWN ERROR'
	    with open(LOG, 'a') as file:
		file.write(z+'\n')
	    sys.exit(e)
