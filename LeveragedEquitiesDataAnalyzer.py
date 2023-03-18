import os
import json
import operator
import decimal
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from matplotlib.ticker import FormatStrFormatter

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

premarketPercentDict = {
    "SOXX/" : [], 
    "QQQ/" : [],
    "FNGS/" : []
}
returnPercentDict = {
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
    startDate = "2021-01-01"
    startIndex = next(x for x, val in enumerate(fileList) if val >= startDate)
    fileList = fileList[startIndex:]
    previousClose = -1

    with open(ticker + fileList[0], "r") as fileReader:
        data = json.load(fileReader)
        previousClose = data["close"]
    fileList.pop(0)
    for file in fileList:
        with open(ticker + file, "r") as fileReader:
            data = json.load(fileReader)
            nextPreviousClose = data["close"]
            premarketPercentDict[ticker].append((data["preMarket"] - previousClose) / previousClose)
            if data["preMarket"] >= previousClose:
                with open(upTickerDict[ticker] + file, "r") as leveragedFileReader:
                    data = json.load(leveragedFileReader)
            else:
                with open(downTickerDict[ticker] + file, "r") as leveragedFileReader:
                    data = json.load(leveragedFileReader)
            returnAmount = data["close"] - data["open"]
            maxAmount = data["high"] - data["open"]
            returnPercentDict[ticker].append(1 + returnAmount / data["open"])
            maxPercentDict[ticker].append(1 + maxAmount / data["open"])
            previousClose = nextPreviousClose

for ticker, list in returnPercentDict.items():
    fig, ax = plt.subplots(1, 3, figsize=(19, 8))
    print(ticker)
    print("Dollar-weighted return: " + str(round(decimal.Decimal(reduce(operator.mul, list, 1)), DECIMAL_PLACES)))
    print("Dollar-weighted return excluding losses: " + str(round(decimal.Decimal(reduce(operator.mul, map(lambda x : max(x, 1), list), 1)), DECIMAL_PLACES)))
    print("Average percent return: " + str(round(decimal.Decimal(sum(list) / len(list)), DECIMAL_PLACES)))
    print("Win percent on closes: " + str(round(decimal.Decimal(sum(1 for i in list if i >= 1) / len(list) * 100), DECIMAL_PLACES)))
    print("Min percent return on closes: " + str(round(decimal.Decimal(min(list)), DECIMAL_PLACES)))
    print("Max percent return on closes: " + str(round(decimal.Decimal(max(list)), DECIMAL_PLACES)))
    maxList = maxPercentDict[ticker]
    print("Max dollar-weighted return: " + str(round(decimal.Decimal(reduce(operator.mul, maxList, 1)), DECIMAL_PLACES)))
    print("Average max percent return: " + str(round(decimal.Decimal(sum(maxList) / len(maxList)), DECIMAL_PLACES)))
    print("Min max percent return: " + str(round(decimal.Decimal(min(maxList)), DECIMAL_PLACES)))
    print("Max max percent return: " + str(round(decimal.Decimal(max(maxList)), DECIMAL_PLACES)))

    counts, bins, patches = ax[0].hist(list, edgecolor='black')
    ax[0].set_title("Average percent returns")
    ax[0].set_xticks(bins)
    ax[0].xaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
    ax[0].tick_params(axis='x', labelsize=8)
    bin_centers = 0.5 * np.diff(bins) + bins[:-1]
    for count, x in zip(counts, bin_centers):
        ax[0].annotate(int(count), xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -18), textcoords='offset points', va='top', ha='center')
        percent = '{:.1%}'.format(float(count) / counts.sum())
        ax[0].annotate(percent, xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -32), textcoords='offset points', va='top', ha='center')

    counts, bins, patches = ax[1].hist(maxList, edgecolor='black')
    ax[1].set_title("Max percent returns")
    ax[1].set_xticks(bins)
    ax[1].xaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
    ax[1].tick_params(axis='x', labelsize=8)
    bin_centers = 0.5 * np.diff(bins) + bins[:-1]
    for count, x in zip(counts, bin_centers):
        ax[1].annotate(int(count), xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -18), textcoords='offset points', va='top', ha='center')
        percent = '{:.1%}'.format(float(count) / counts.sum())
        ax[1].annotate(percent, xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -32), textcoords='offset points', va='top', ha='center')

    counts, bins, patches = ax[2].hist(premarketPercentDict[ticker], edgecolor='black')
    ax[2].set_title("Premarket percents")
    ax[2].set_xticks(bins)
    ax[2].xaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
    ax[2].tick_params(axis='x', labelsize=8)
    bin_centers = 0.5 * np.diff(bins) + bins[:-1]
    for count, x in zip(counts, bin_centers):
        ax[2].annotate(int(count), xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -18), textcoords='offset points', va='top', ha='center')
        percent = '{:.1%}'.format(float(count) / counts.sum())
        ax[2].annotate(percent, xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -32), textcoords='offset points', va='top', ha='center')

    plt.suptitle(ticker[:-1])

plt.show()