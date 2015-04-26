from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import  WebElement
import time
from bs4 import BeautifulSoup
import re
from datetime import date, timedelta

class WaterScrapper:
    def __init__(self, date, countyName):
        self._date = date
        self._countyName = countyName
        self._timeDelay = 1
        self._initialTimeDelay = 10
        self._finalTimeDelay = 10
        self._url = "https://wins.mwdsc.org/Unsecured/login.aspx?Wamiuser=Wamiuser"
        self._reportLinkID = 'ctl00_ContentPlaceHolder1_gridReports_ctl05_ReportNameLinkButton'
        self._countySelectID = 'ctl00_ContentPlaceHolder1_ddlMember'
        self._meterSelectID = 'ctl00_ContentPlaceHolder1_ddlMeter'
        self._startDateID = 'ctl00_ContentPlaceHolder1_txtStart'
        self._endDateID = 'ctl00_ContentPlaceHolder1_txtEnd'
        self._previewReportButtonID = 'ctl00_ContentPlaceHolder1_PreviewRptLinkButton'
        self._externalFrameID = 'documentFrame000hb'
        self._internalFrameID = 'ceframe'
        self._containerDivClassPattern = re.compile("adi4g")
        self._meterDataClassPattern = re.compile("fci4g")

        self._driver = webdriver.Firefox()
        self._driver.implicitly_wait(self._initialTimeDelay) # seconds
        self._driver.get(self._url)
        # self._wait for loading form
        self._wait = WebDriverWait(self._driver, self._initialTimeDelay)
        self._iterator = 0;

    def startEngine(self):

        # Get anchor link for report form
        reportLink = self._wait.until(EC.element_to_be_clickable((By.ID,self._reportLinkID)))
        # Click report link
        reportLink.send_keys(Keys.RETURN)
        time.sleep(self._timeDelay)

        try:
            countyTag = self._wait.until(EC.presence_of_element_located((By.ID,self._countySelectID)))
            countySelectTag = Select(countyTag)
            countySelectTag.select_by_value(self._countyName)
        except Exception as e:
            return self.handleException("County Name", e)

        time.sleep(self._timeDelay)

        try:
            meterTag = self._wait.until(EC.presence_of_element_located((By.ID,self._meterSelectID)))
            meterSelectTag = Select(meterTag)
            meterSelectTag.select_by_value('All')
        except Exception as e:
            return self.handleException("Meter", e)

        time.sleep(self._timeDelay)

        if self._iterator < 1:
            startDateInputField = self._driver.find_element_by_id(self._startDateID)
            startDateInputField.send_keys(self._date)
            time.sleep(self._timeDelay)

            endDateInputField = self._driver.find_element_by_id(self._endDateID)
            endDateInputField.send_keys(self._date)
            time.sleep(self._timeDelay)

        previewReportButton = self._driver.find_element_by_id(self._previewReportButtonID)
        previewReportButton.send_keys(Keys.RETURN)
        #time.sleep(self._finalTimeDelay)

        currentWindow = self._driver.current_window_handle
        popupWindow = None
        windows = self._driver.window_handles

        while len(windows) < 2:
            print "==Windows: " + str(len(windows))
            windows = self._driver.window_handles

        for window in windows:
            if currentWindow != window:
                popupWindow = window
        self._driver.switch_to.window(popupWindow)

        externalFrame = self._driver.find_element_by_name(self._externalFrameID)
        self._driver.switch_to.frame(externalFrame)
        internalFrame = self._driver.find_element_by_name(self._internalFrameID)
        self._driver.switch_to.frame(internalFrame)
        cridReportPage = self._wait.until(EC.presence_of_element_located((By.ID,'cridreportpage')))

        soup = BeautifulSoup(self._driver.page_source)
        self._driver.close()
        self._driver.switch_to.window(self._driver.window_handles[0])
        containerDivs = soup.findAll('div', {"class": self._containerDivClassPattern})

        actualSpanIndex = None
        iterator = 0
        for div in containerDivs:
            try:
                title = div["title"]
            except KeyError:
                title = ""
            if (title == "Visit the Support Site for samples, web forums, tutorials, technical briefs and more!"):
                actualSpanIndex = iterator - 1
            iterator = iterator + 1
        if actualSpanIndex == None:
            return self.handleException("Could not find frame", None)

        newSoup = BeautifulSoup(str(containerDivs[actualSpanIndex]))
        span = newSoup.find('span', {"class": self._meterDataClassPattern})
        self._iterator = self._iterator + 1
        return {'status': 'true', 'value': str(span.text.encode('utf-8'))}

    def handleException(self, message, exception):
        self._driver.get(self._url)
        self._iterator = 0;
        #print "Exception caught while: " + message
        #print exception
        #print "======= Let's try again ======="
        return {'status': 'false'}

def main():
    fileName = 'meterData.txt'
    yesterday = date.today() - timedelta(days=1)
    dateString = str(yesterday.month) +"/"+ str(yesterday.day) + "/" + str(yesterday.year)
    scrapper = WaterScrapper(dateString, 'B')

    appender = open(fileName, 'a')
    reader = open('CountyNames.txt', 'r')

    if reader.mode == 'r' and appender.mode == 'a':
        competeListing = reader.readlines()
        for line in competeListing:
            stringList = line.split(',')
            key = stringList[0]
            valueList = stringList[1].split('\n')
            value = valueList[0]
            scrapper._countyName = key

            data = scrapper.startEngine()
            while(data['status'] == 'false'):
                time.sleep(1*5)
                data = scrapper.startEngine()

            grandTotal = re.findall('grand', data['value'], re.IGNORECASE)
            if grandTotal:
                data['value'] = 'NA'
            formattedLine = dateString + ", " + value + ", "  + data['value'] + "\n"
            print dateString + ", " + value + ", "  + data['value'] + ' AF'
            appender.write(formattedLine)

    appender.close()
    reader.close()

if __name__ == "__main__": main()
