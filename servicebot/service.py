from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import getpass

#login info
eid = raw_input('Enter your EID: ')
email = raw_input('Enter your work email: ')
pw = getpass.getpass(prompt='Password: ')

driver = webdriver.Chrome()

# Get Slack Page
driver.get('https://utservicedesk.slack.com/')
driver.implicitly_wait(5)
element = driver.find_element_by_name("email")
element.send_keys(email)
element = driver.find_element_by_name("password")
element.send_keys(pw)
driver.find_element_by_id("signin_btn").click()

# Get UTEID Manager Tab
driver.execute_script("window.open('https://idmanager.its.utexas.edu/eid_admin/', 'tab1')")
driver.implicitly_wait(5)
driver.switch_to_window(driver.window_handles[1])
element = driver.find_element_by_name("IDToken1")
element.clear()
element.send_keys(eid)
element = driver.find_element_by_name("IDToken2")
element.clear()
element.send_keys(pw)
driver.find_element_by_name("Login.Submit").click()
driver.find_element_by_id("IDToken0").click()
driver.find_element_by_name("Login.Submit").click()

# Get UTBox Page
driver.execute_script("window.open('https://utexas.app.box.com/folder/0', 'tab2')")
driver.switch_to_window(driver.window_handles[2])
driver.find_element_by_tag_name('button').click()
driver.implicitly_wait(5)
element = driver.find_element_by_name("j_username")
element.clear()
element.send_keys(eid)
element = driver.find_element_by_name("j_password")
element.clear()
element.send_keys(pw)
driver.find_element_by_name("_eventId_proceed").click()

# Get UTService Now Page
driver.execute_script("window.open('https://ut.service-now.com/', 'tab3')")
