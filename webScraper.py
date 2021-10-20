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

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

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

def getElementAt(index,elements):
  i = 0
  for element in elements:
    if(i == index): return element
    i=i+1

def get_page():
  for element in chrome.find_elements_by_xpath("//div[@class='transaction-row']//div[@class='transaction--content-wrapper']"):
      elements = element.find_elements_by_xpath(".//div[@class='transaction--desc']//div[@class='transaction--desc-row']")
      orderNum = getElementAt(0,elements)
      nameElement = getElementAt(1,elements)
      netElement  = element.find_element_by_xpath(".//div[@class='transaction--net']")
      #print("I am here")
      if "Shipping" not in orderNum.text and "Payout" not in orderNum.text and "INTERNAL_TRANSFER" not in orderNum.text:
        order = orderNum.text[6:]
        name = nameElement.text
        net = netElement.text
        items[order]={"Order Number":order,"Name":name,"Net":net}
        #print(items[order])
  for element in chrome.find_elements_by_xpath("//div[@class='transaction-row']//div[@class='transaction--content-wrapper']"):
      orderNum = element.find_element_by_xpath(".//div[@class='transaction--desc']//div[@class='transaction--desc-row']")
      amountElement = element.find_element_by_xpath(".//div[@class='transaction--amount']")
      if "Shipping" in orderNum.text and "Refund" not in orderNum.text:
          order = orderNum.text[len(orderNum.text)-14:]
          amount = amountElement.text
          shipping.append({"Order Number": order, "Amount":amount})


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73'
options = webdriver.ChromeOptions()
#options.headless = Tru
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--log-level=1')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
chrome = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

SERVICE_ACCOUNT_FILE = 'keys.json'
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1r9uRW8T74x-hrURdwiNH-gqvZZRZyosei0o4jj4B-Os'
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

shipping = []
items = {}
items['items1'] = {'Order Number':'','Name':'name','Net':0}

load_cookies(chrome,"cookies.txt","https://signin.ebay.com")
time.sleep(2)
chrome.get("https://signin.ebay.com")
time.sleep(2)
chrome.get("https://www.ebay.com/mes/transactionlist")
time.sleep(2)

button = chrome.find_element_by_xpath("//div[@class='transactions-pagination']//nav[@class='pagination']//button[@class='icon-btn pagination__next']")
#time.sleep(1)
#button.click()
save_cookies(chrome,"cookies.txt")






get_page()
while button.value_of_css_property('color') == "rgba(17, 24, 32, 1)" :
  button.click()
  time.sleep(2)
  get_page()
  
  
  
itemList = []
for dic in shipping:
    orderNum = dic["Order Number"]
    if(orderNum in items):
      print("made it here")
      amount = round((float(items[orderNum]["Net"][1:]) - float(dic["Amount"][2:])),2)
      itemList.append([items[orderNum]["Name"],orderNum,amount])
print(itemList)

request = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A2", valueInputOption="USER_ENTERED",body={"values":itemList})
response = request.execute()




























#driver.get("https://facebook.com")
#cookies = getCookies("cookies.csv")
#for cookie in cookies:
  #print(cookie)
  #driver.add_cookie(cookie)
#for cookie in driver.get_cookies():
  #print(cookie)
#time.sleep(4)
#driver.refresh()
#login = driver.find_element_by_xpath("//input[@class='inputtext _55r1 _6luy']")
#print(login.get_attribute("class"))
#login.send_keys("varunwadhwa.1822@gmail.com")
#password = driver.find_element_by_xpath("//input[@class='inputtext _55r1 _6luy _9npi']")
#password.send_keys("vaDavis1822#")
#driver.find_element_by_xpath("//button[@class='_42ft _4jy0 _6lth _4jy6 _4jy1 selected _51sy']").click()














#def getCookies(file):
  #with open("cookies.csv",encoding = 'utf-8-sig') as f:
    #dictReader = csv.DictReader(f)
    #cookies = list(dictReader)
    #print(cookies)
  #return cookies


#driver.get("https://signin.ebay.com")
#print(driver.get_cookies())
#element = WebDriverWait(driver, 100).until(
      #EC.presence_of_element_located((By.ID, "userid"))
  #)
#time.sleep(2)
#driver.get("https://signin.ebay.com")
#driver.find_element_by_id("userid").send_keys("varunwadhwa.1822@gmail.com")
#time.sleep(2)
#driver.find_element_by_id("signin-continue-btn").click()
#time.sleep(2)
#driver.find_element_by_id("pass").send_keys("vaDavis1822#")
#time.sleep(2)
#driver.find_element_by_id("sgnBt").click()
#time.sleep(2)
#driver.find_element_by_id("pass")
#driver.get("https://www.ebay.com/mes/transactionlist")
#for cookie in driver.get_cookies():
  #print(cookie)
  #driver.add_cookie(cookie)
#time.sleep(2)


#driver.get("https://signin.ebay.com")



#time.sleep(1)
#element = driver.find_element_by_xpath("//div[@aria-label='Sign in with Google']")
#time.sleep(.5)
#element.click()
#fields = driver.find_elements_by_tag_name("input")
#driver.find_element_by_name("identifier").send_keys("varunwadhwa.1822@gmail.com")
#driver.find_element_by_xpath("//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qIypjc TrZEUc lw1w4b']").click()
#time.sleep(4)
#driver.get_screenshot_as_file("test.png")

#for cookie in driver.get_cookies(): 
  #print(cookie)
  #driver.add_cookie(cookie)
#driver.add_cookie({'domain':'.hcaptcha.com', 'name': 'hc_accessibility', 'path': '/','send for' : 'secure_connections_only','value': 'QMOUs2qLNtIj268f9KKRIplIEatP/GUt6UR9AmwHlxwY61OrAgO4L7MaaWUptx6LxHHbl0mdbxFJzAcaOGVnBTmjnCB8Zc0j7ki09DGUqMjxB5y3K83QcQcQBgnOF9mYepk7ISHXc1eN2zB1E6nlkdal+vup4CF4OQYg5hIjazo9LVE0pLuMDtcivqquMW8N/8UDRO2IhDizO2SHUbabKFv9vCGxg4NMm1SrOxFylZDM2YZGKh1gTk2mMThxQeLpp1/jXoF+bCfL6R0a2limCGgwNGK9kWLUTZOdnmtu3/uwTmaM8fmL9aTnEIaFTysE3OoXxJiE0fqT8e4EjGPLdqHbEwUEgM15lqJWqxS7/jMZ6vBt7mteCWoxycjpLZJvQ1cUaxg9jQrRr9YOgxwkCF2bBrnmgBFpSGT0FxKnw38tqFrykEeJhkb8nIKDsdFinHH5Ji/WS/aq2MbHYDWp85dZ3SqaqSs3IsImdSfGiJwV6SCsS/RLtZUHYnjzCh3Bu+XM0/cjdrpjOF+wpP8n8GCURLA=ficr5I5MCrawYcNS'})
#driver.add_cookie()
#for cookie in getCookies("cookies.csv"):
  #driver.add_cookie(cookie)
#driver.switch_to.frame(0)
#print(driver.page_source)
#element = driver.find_element_by_id("anchor")
#element.click()
#time.sleep(1)
#print("here")
#driver.refresh()
#driver.get_screenshot_as_file("screenshot3.png")
#print(element.get_attribute("title"))
#print(driver.page_source)

#for cookie in driver.get_cookies():
 # driver.add_cookie(cookie)
#driver.switch_to_frame("0ixz7c8u82i7")
#element = driver.find_elements_by_id("0ixz7c8u82i7")
#driver.get("https://api.hcaptcha.com/getcaptcha?s=195eeb9f-8f50-4a9c-abfc-a78ceaa3cdde")
#driver.get_screenshot_as_file("screenshot.png")
#print(driver.get_cookies())

#links = driver.find_elements_by_tag_name("a")
#for link in links:
 #   if not link.is_displayed():
  #      print("The link "+link.get_attribute("href")+" is a trap")
#fields = driver.find_element_by_name('rqid')
#for field in fields:
 #   print(field.get_attribute("name"))