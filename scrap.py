import pickle
import pprint
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from selenium.webdriver.remote.webelement import WebElement


def save_cookies(driver, location):

    pickle.dump(driver.get_cookies(), open(location, "wb"))


def load_cookies(driver, location, url=None):

    cookies = pickle.load(open(location, "rb"))
    driver.delete_all_cookies()
    # have to be on a page before you can add any cookies, any page - does not matter which
    driver.get("https://google.com" if url is None else url)
    for cookie in cookies:
        if isinstance(cookie.get('expiry'), float):#Checks if the instance expiry a float 
            cookie['expiry'] = int(cookie['expiry'])# it converts expiry cookie to a int 
        driver.add_cookie(cookie)


def delete_cookies(driver, domains=None):

    if domains is not None:
        cookies = driver.get_cookies()
        original_len = len(cookies)
        for cookie in cookies:
            if str(cookie["domain"]) in domains:
                cookies.remove(cookie)
        if len(cookies) < original_len:  # if cookies changed, we will update them
            # deleting everything and adding the modified cookie object
            driver.delete_all_cookies()
            for cookie in cookies:
                driver.add_cookie(cookie)
    else:
        driver.delete_all_cookies()


# Path where you want to save/load cookies to/from aka C:\my\fav\directory\cookies.txt
cookies_location = "cookies.txt"
# Initial load of the domain that we want to save cookies for
chrome = webdriver.Chrome(executable_path="chromedriver.exe")
delete_cookies(chrome)
chrome.get("https://signin.ebay.com")
#print(driver.get_cookies())
element = WebDriverWait(chrome, 100).until(
      EC.presence_of_element_located((By.ID, "userid"))
  )
time.sleep(2)
#driver.get("https://signin.ebay.com")
chrome.find_element_by_id("userid").send_keys("varunwadhwa.1822@gmail.com")
time.sleep(2)
chrome.find_element_by_id("signin-continue-btn").click()
time.sleep(2)
chrome.find_element_by_id("pass").send_keys("vaDavis1822#")
time.sleep(2)
chrome.find_element_by_id("sgnBt").click()
time.sleep(2)

save_cookies(chrome, cookies_location)
chrome.quit()

# Load of the page you cant access without cookies, this one will fail
#chrome = webdriver.Chrome()
#chrome.get("")


# Load of the page you cant access without cookies, this one will go through
chrome = webdriver.Chrome()
load_cookies(chrome, cookies_location,"https://signin.ebay.com")
time.sleep(2)
chrome.get("https://signin.ebay.com")

# chrome = webdriver.Chrome()
# chrome.get("https://google.com")
# time.sleep(2)
# pprint.pprint(chrome.get_cookies())
# print "=========================\n"
#
# delete_cookies(chrome, domains=["www.google.com"])
# pprint.pprint(chrome.get_cookies())
# print "=========================\n"
#
# delete_cookies(chrome)
# pprint.pprint(chrome.get_cookies())