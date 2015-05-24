import pymongo
from pymongo import MongoClient
import math

def computeMedian(countyDocuments, dataKey):
    medianDocument = countyDocuments[countyDocuments.count()/2]
    print "Medain==> ",
    print "Date: " + str(medianDocument["Date"]) + " ",
    if (medianDocument[dataKey] != "NA"):
        print dataKey+ ": " + medianDocument[dataKey]
    if (medianDocument[dataKey] == "NA"):
        print dataKey+ ": NA"
    return medianDocument

def computeMeanAndMode(countyDocuments, dataKey):
    dataLength = 0.0
    dataSummation = 0.0
    mode = {0.00: 0};
    for document in countyDocuments:
        if (document[dataKey] != "NA"):
            dataLength = dataLength + 1.0
            dataSummation = dataSummation + float(document[dataKey].replace(",", ""))
            newEntry = "true"
            for modeKey in mode:
                if(float(modeKey) == float(document[dataKey].replace(",", ""))):
                    mode[modeKey] = mode[modeKey] + 1
                    newEntry = "false"
            if(newEntry == "true"):
                mode[float(document[dataKey].replace(",", ""))] = 1
        # if (document[dataKey] == "NA"):
            # print "Not Considering"
    
    mean = dataSummation/dataLength
    print "Mean==> " + str(mean)
    print "Mode==> "
    for modeKey in mode:
        print str(float(modeKey)) + " : " + str(int(mode[modeKey]))

    result = {"mean": mean, "mode": mode}
    return result

def computeStandardDeviation(countyDocuments, dataKey, mean):
    dataLength = 0.0
    standardDeviationSummation = 0.0
    for document in countyDocuments:
        if (document[dataKey] != "NA"):
            dataLength = dataLength + 1.0
            value = float(document[dataKey].replace(",", ""))
            standardDeviationSummation = standardDeviationSummation + ((value-mean) * (value-mean))
        # if (anaheimData['Rain'] == "NA"):
        #     print "Not Considering"
    standardDeviation = math.sqrt(standardDeviationSummation / dataLength)
    print "Standard Deviation==> " + str(standardDeviation)
    return standardDeviation

def statisticalEngine(countyName):
    client = MongoClient('localhost', 27017)
    db = client['cs-594-project']
    
    print "Rain Data (in)"
    weatherCollection = db['weatherData']
    computeMedian(weatherCollection.find({"City": countyName}).sort("Date", pymongo.DESCENDING), "Rain")
    meanAndMode = computeMeanAndMode(weatherCollection.find({"City": countyName}), "Rain")
    computeStandardDeviation(weatherCollection.find({"City": countyName}), "Rain", meanAndMode["mean"])

    print ""
    print "Water Consumption Data (AF)"
    waterCollection = db['waterData']
    computeMedian(waterCollection.find({"City": countyName}).sort("Date", pymongo.DESCENDING), "Water")
    meanAndMode = computeMeanAndMode(waterCollection.find({"City": countyName}), "Water")
    computeStandardDeviation(waterCollection.find({"City": countyName}), "Water", meanAndMode["mean"])
    
def main():
    client = MongoClient('localhost', 27017)
    db = client['cs-594-project']
    weatherCollection = db['weatherData']
    for countyName in weatherCollection.find().distinct("City"):
        print "====================="
        print countyName
        print " "
        statisticalEngine(countyName)
        print "====================="

if __name__ == "__main__": main()