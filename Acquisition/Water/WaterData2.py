from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re

timeDelay = 6
driver = webdriver.Firefox()
driver.implicitly_wait(timeDelay*5) # seconds
url = "https://wins.mwdsc.org/Unsecured/login.aspx?Wamiuser=Wamiuser"
driver.get(url)

wait = WebDriverWait(driver, 20)
elemReport = wait.until(EC.element_to_be_clickable((By.ID,'ctl00_ContentPlaceHolder1_gridReports_ctl05_ReportNameLinkButton')))
elemReport.send_keys(Keys.RETURN)

print "Selecting All"
elemMeter = wait.until(EC.element_to_be_clickable((By.ID,'ctl00_ContentPlaceHolder1_ddlMeter')))
elemMeterselect = Select(elemMeter)
elemMeterselect.select_by_value('All')
print "Selected All"

time.sleep(timeDelay)

print "Entering Start Date"
#elemStartDate = wait.until(EC.element_to_be_clickable((By.ID, 'ctl00_ContentPlaceHolder1_txtStart'))
elemStartDate = driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtStart')
elemStartDate.send_keys('4/1/2015')
print "Entered Start Date"

time.sleep(timeDelay)

print "Entering End Date"
#elemEndDate = wait.until(EC.element_to_be_clickable(('ctl00_ContentPlaceHolder1_txtEnd'))
elemEndDate = driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtEnd')
elemEndDate.send_keys('4/1/2015')
print "Entered End Date"

time.sleep(timeDelay)

#elemPreviewReport = wait.until(EC.element_to_be_clickable(('ctl00_ContentPlaceHolder1_PreviewRptLinkButton'))
elemPreviewReport = driver.find_element_by_id('ctl00_ContentPlaceHolder1_PreviewRptLinkButton')
elemPreviewReport.send_keys(Keys.RETURN)


time.sleep(timeDelay*10)
currentWindow = driver.current_window_handle
popupWindow = None
windows =	driver.window_handles
for window in windows:
	if currentWindow != window:
		print "Setting popup window"
		popupWindow = window

driver.switch_to.window(popupWindow)

elemExternalFrame = driver.find_element_by_name('documentFrame000hb')
driver.switch_to.frame(elemExternalFrame)
elemInternalFrame = driver.find_element_by_name('ceframe')
driver.switch_to.frame(elemInternalFrame)
#print driver.page_source

soup = BeautifulSoup(driver.page_source)
# f = open("rawData.txt","w+")
# f.write(soup.prettify().encode('utf-8') + "\n")
# f.close()

spanTags = soup.findAll('div', {"style": 'z-index:25;top:367px;left:667px;width:77px;height:15px;text-align:right;'});
# print spanTags
newSoup = BeautifulSoup(str(spanTags[0]))
print newSoup.prettify()
span = newSoup.find('span', {"class": re.compile("fci4g")});
f = open("data.txt","w+")
f.write(span.text.encode('utf-8') + "\n")
f.close()

# spanTags = soup.findAll('span', {"class": re.compile("fci4g5*-4")});

# f = open("data.txt","w+")
# for span in spanTags:
# 	f.write(span.encode('utf-8') + "\n")
# 	#print span.text
# f.close()
#fci4g5h

