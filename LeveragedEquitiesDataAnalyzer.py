import os
import json
import operator
from functools import reduce

tickerList = ["SOXX/", "QQQ/", "FNGS/"]
upTickerDict = {
    "SOXX/" : "SOXL/", 
    "QQQ/" : "TQQQ/",
    "FNGS/" : "FNGU/"
}
downTickerDict = {
    "SOXX/" : "SOXS/", 
    "QQQ/" : "SQQQ/",
    "FNGS/" : "FNGD/"
}

returnAmountDict = {
    "SOXX/" : [], 
    "QQQ/" : [],
    "FNGS/" : []
}
returnPercentDict = {
    "SOXX/" : [], 
    "QQQ/" : [],
    "FNGS/" : []
}

for ticker in tickerList:
    numberHighsBelowOpens = 0
    fileList = os.listdir(ticker)
    previousClose = -1
    with open(ticker + fileList[0], "r") as fileReader:
        data = json.load(fileReader)
        previousClose = data["close"]
    fileList.pop(0)
    for file in fileList:
        with open(ticker + file, "r") as fileReader:
            data = json.load(fileReader)
            nextPreviousClose = data["close"]
            if data["preMarket"] >= previousClose:
                with open(upTickerDict[ticker] + file, "r") as leveragedFileReader:
                    data = json.load(leveragedFileReader)
            else:
                with open(downTickerDict[ticker] + file, "r") as leveragedFileReader:
                    data = json.load(leveragedFileReader)
            returnAmount = data["close"] - data["open"]
            returnAmountDict[ticker].append(returnAmount)
            returnPercentDict[ticker].append(1 + returnAmount / data["open"])
            previousClose = nextPreviousClose

for ticker, list in returnPercentDict.items():
    print(ticker)
    print(reduce(operator.mul, list, 1))
    print(sum(list) / len(list))