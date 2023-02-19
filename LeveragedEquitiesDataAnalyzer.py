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
    fileList = os.listdir(ticker)
    previousClose = -1
    with open(ticker + fileList[0], "r") as fileReader:
        data = json.load(fileReader)
        previousClose = data['close']
    fileList.pop(0)
    for file in fileList:
        with open(ticker + file, "r") as fileReader:
            data = json.load(fileReader)
            if data['preMarket'] >= previousClose:
                with open(upTickerDict[ticker] + file, "r") as leveragedFileReader:
                    data = json.load(leveragedFileReader)
                    returnAmount = data["close"] - data["open"]
                    returnAmountDict[ticker].append(returnAmount)
                    returnPercentDict[ticker].append(1 + returnAmount / data["open"])
            else:
                with open(downTickerDict[ticker] + file, "r") as leveragedFileReader:
                    data = json.load(leveragedFileReader)
                    returnAmount = data["close"] - data["open"]
                    returnAmountDict[ticker].append(returnAmount)
                    returnPercentDict[ticker].append(1 + returnAmount / data["open"])

for ticker, list in returnPercentDict.items():
    print(reduce(operator.mul, list, 1))