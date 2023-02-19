import os
import json
import operator
import decimal
from functools import reduce

DECIMAL_PLACES = 4

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
maxAmountDict = {
    "SOXX/" : [],
    "QQQ/" : [],
    "FNGS/" : []
}
maxPercentDict = {
    "SOXX/" : [],
    "QQQ/" : [],
    "FNGS/" : []
}

for ticker in tickerList:
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
            maxAmount = data["high"] - data["open"]
            returnAmountDict[ticker].append(returnAmount)
            maxAmountDict[ticker].append(maxAmount)
            returnPercentDict[ticker].append(1 + returnAmount / data["open"])
            maxPercentDict[ticker].append(1 + maxAmount / data["open"])
            previousClose = nextPreviousClose

for ticker, list in returnPercentDict.items():
    print(ticker)
    print("Dollar-weighted return: " + str(round(decimal.Decimal(reduce(operator.mul, list, 1)), DECIMAL_PLACES)))
    print("Dollar-weighted return exluding losses: " + str(round(decimal.Decimal(reduce(operator.mul, map(lambda x : max(x, 1), list), 1)), DECIMAL_PLACES)))
    print("Average percent return: " + str(round(decimal.Decimal(sum(list) / len(list)), DECIMAL_PLACES)))
    print("Min average percent return: " + str(round(decimal.Decimal(min(list)), DECIMAL_PLACES)))
    print("Max average percent return: " + str(round(decimal.Decimal(max(list)), DECIMAL_PLACES)))
    maxList = maxPercentDict[ticker]
    print("Max dollar-weighted return: " + str(round(decimal.Decimal(reduce(operator.mul, maxList, 1)), DECIMAL_PLACES)))
    print("Average max percent return: " + str(round(decimal.Decimal(sum(maxList) / len(maxList)), DECIMAL_PLACES)))
    print("Min max percent return: " + str(round(decimal.Decimal(min(maxList)), DECIMAL_PLACES)))
    print("Max max percent return: " + str(round(decimal.Decimal(max(maxList)), DECIMAL_PLACES)))