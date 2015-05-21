import urllib2
import json
from datetime import datetime, date, timedelta
import pymongo
from pymongo import MongoClient

class WeatherApiConsumer:
	def __init__(self, date, countyName):
		self._date = date
		self._countyName = countyName
		
	def getPrecipitationInInches(self):
		url = 'http://api.wunderground.com/api/cc7750cde6c9a984/history_'+ str(self._date) +'/q/CA/'+ str(self._countyName) +'.json'
		response = urllib2.urlopen(url)
		jsonString = response.read()
		parsedJson = json.loads(jsonString)
		dailySummary = parsedJson['history']['dailysummary'][0]
		rain = dailySummary['precipi']
		response.close()
		return rain

def engine(selectedDate):
	client = MongoClient('localhost', 27017)
	db = client['cs-594-project']
	weatherCollection = db['weatherData']
	fileName = 'weatherData.txt'
	dateString = date.strftime('%Y%m%d')
	consumer = WeatherApiConsumer(dateString, 'Anaheim')
	
	appender = open(fileName, 'a')
	reader = open('CountyNames.txt', 'r')

	if reader.mode == 'r' and appender.mode == 'a':
		competeListing = reader.readlines()
		for line in competeListing:
			stringList = line.split(',')
			key = stringList[0]
			valueList = stringList[1].split('\n')
			value = valueList[0]
			consumer._countyName = value.lstrip(' ').replace(' ', '_')
			data = consumer.getPrecipitationInInches()
			if data == 'T':
				data = 'NA'
			formattedLine = dateString + ", " + value + ", "  + data + "\n"
			print dateString + ", " + value + ", "  + data + " in" 
			appender.write(formattedLine)
			weatherCollection.insert({"Date": dateString, "City": value, "Rain": data})

	appender.close()
	reader.close()

def main():
	januaryFirst = datetime(2015, 1, 1, 00,00,00).date()
	daysCount = date.today()-januaryFirst
	#print daysCount
	for iterator in range(0, daysCount.days):
		print "========"
		selectedDate = date.today() - timedelta(days=iterator)
		engine(selectedDate)
		print "========"

if __name__ == "__main__": main()
