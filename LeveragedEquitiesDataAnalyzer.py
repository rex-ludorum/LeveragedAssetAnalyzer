import json
import operator
import decimal
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from matplotlib.ticker import FormatStrFormatter

DECIMAL_PLACES = 4

tickerList = ["SOXX", "QQQ", "FNGS", "SPY", "XLF", "VGT", "VTWO", "XBI", "TLT", "DIA", "FXI", "FDN", "EEM", "SPHB", "IYR", "MDY", "IEF", "GDX", "GDXJ", "IEO"]

upTickerDict = {
	"SOXX" : "SOXL",
	"QQQ" : "TQQQ",
	"SPY" : "SPXL",
	"VGT" : "TECL",
	"VTWO" : "TNA",
	"XBI" : "LABU",
	"TLT" : "TMF",
	"DIA" : "UDOW",
	"FXI" : "YINN",
	"FDN" : "WEBL",
	"EEM" : "EDC",
	"SPHB" : "HIBL",
	"IYR" : "DRN",
	"MDY" : "UMDD",
	"IEF" : "TYD",
	# try two different sets of premarket data for gold
	"GDX" : "GDXU",
	"GDXJ" : "GDXU",
	"IEO" : "OILU",
	# TODO: handle both cases together?
	# FNG* and BULZ/BERZ are all FANG assets
	"FNGS" : "FNGU",
	# "FNGS" : "BULZ",
	# FA* tracks large-cap financial companies while BNK* tracks US large banks
	# however, they perform similarly
	"XLF" : "FAS",
	# "XLF" : "BNKU",
}

downTickerDict = {
	"SOXX" : "SOXS",
	"QQQ" : "SQQQ",
	"SPY" : "SPXS",
	"VGT" : "TECS",
	"VTWO" : "TZA",
	"XBI" : "LABD",
	"TLT" : "TMV",
	"DIA" : "SDOW",
	"FXI" : "YANG",
	"FDN" : "WEBS",
	"EEM" : "EDZ",
	"SPHB" : "HIBS",
	"IYR" : "DRV",
	"MDY" : "SMDD",
	"IEF" : "TYO",
	"GDX" : "GDXD",
	"GDXJ" : "GDXD",
	"IEO" : "OILD",
	"FNGS" : "FNGD",
	# "FNGS" : "BERZ",
	"XLF" : "FAZ",
	# "XLF" : "BNKD",
}

premarketPercentDict = {
	"SOXX" : [],
	"QQQ" : [],
	"SPY" : [],
	"XLF" : [],
	"VGT" : [],
	"VTWO" : [],
	"XBI" : [],
	"TLT" : [],
	"DIA" : [],
	"FXI" : [],
	"FDN" : [],
	"EEM" : [],
	"SPHB" : [],
	"IYR" : [],
	"MDY" : [],
	"IEF" : [],
	"FNGS" : [],
	"GDX" : [],
	"GDXJ" : [],
	"IEO" : [],
}

returnPercentDict = {
	"SOXX" : [],
	"QQQ" : [],
	"SPY" : [],
	"XLF" : [],
	"VGT" : [],
	"VTWO" : [],
	"XBI" : [],
	"TLT" : [],
	"DIA" : [],
	"FXI" : [],
	"FDN" : [],
	"EEM" : [],
	"SPHB" : [],
	"IYR" : [],
	"MDY" : [],
	"IEF" : [],
	"FNGS" : [],
	"GDX" : [],
	"GDXJ" : [],
	"IEO" : [],
}

maxPercentDict = {
	"SOXX" : [],
	"QQQ" : [],
	"SPY" : [],
	"XLF" : [],
	"VGT" : [],
	"VTWO" : [],
	"XBI" : [],
	"TLT" : [],
	"DIA" : [],
	"FXI" : [],
	"FDN" : [],
	"EEM" : [],
	"SPHB" : [],
	"IYR" : [],
	"MDY" : [],
	"IEF" : [],
	"FNGS" : [],
	"GDX" : [],
	"GDXJ" : [],
	"IEO" : [],
}

datesDict = {
	"SOXX" : [],
	"QQQ" : [],
	"SPY" : [],
	"XLF" : [],
	"VGT" : [],
	"VTWO" : [],
	"XBI" : [],
	"TLT" : [],
	"DIA" : [],
	"FXI" : [],
	"FDN" : [],
	"EEM" : [],
	"SPHB" : [],
	"IYR" : [],
	"MDY" : [],
	"IEF" : [],
	"FNGS" : [],
	"GDX" : [],
	"GDXJ" : [],
	"IEO" : [],
}

thresholdReturnsDict = {
	"SOXX" : [],
	"QQQ" : [],
	"SPY" : [],
	"XLF" : [],
	"VGT" : [],
	"VTWO" : [],
	"XBI" : [],
	"TLT" : [],
	"DIA" : [],
	"FXI" : [],
	"FDN" : [],
	"EEM" : [],
	"SPHB" : [],
	"IYR" : [],
	"MDY" : [],
	"IEF" : [],
	"FNGS" : [],
	"GDX" : [],
	"GDXJ" : [],
	"IEO" : [],
}

# concatenate a list of dates into a string for printing
def concatDates(dateIndices, dates):
	ret = dates[dateIndices[0]]
	for idx in dateIndices[1:]:
		ret += ', '
		ret += dates[idx]
	return ret

for ticker in tickerList:
	previousClose = -1
	previousDate = ""

	startDate = "2021-01-01"

	with open("data/" + ticker, "r") as fileReader, open("data/" + upTickerDict[ticker], "r") as upFileReader, open("data/" + downTickerDict[ticker], "r") as downFileReader:
		data = json.load(fileReader)
		upData = json.load(upFileReader)
		downData = json.load(downFileReader)

	match ticker:
		# start later on these assets b/c premarket data goes back earlier than the return data
		case "FNGS/":
			# only for BULZ/BERZ, FNGD and FNGU have complete data
			if upTickerDict[ticker] == "BULZ/":
				startDate = max(startDate, "2021-08-17")
		case _:
			pass

	for date, value in data.items():
		if date < startDate:
			continue

		if previousClose == -1:
			previousClose = value['close']
			continue
		if previousDate:
			assert(date > previousDate)
		previousDate = date
		nextPreviousClose = value["close"]
		premarketPercentDict[ticker].append(100 * (value["preMarket"] - previousClose) / previousClose)
		if value["preMarket"] >= previousClose:
			value = upData[date]
		else:
			value = downData[date]
		returnAmount = value["close"] - value["open"]
		maxAmount = value["high"] - value["open"]
		returnPercentDict[ticker].append(1 + returnAmount / value["open"])
		maxPercentDict[ticker].append(1 + maxAmount / value["open"])
		previousClose = nextPreviousClose
		datesDict[ticker].append(date)

thresholds = list(range(0, 500, 25))
thresholds.pop(0)
thresholds.append(500)

for ticker in tickerList:
	for threshold in thresholds:
		premarketDict = premarketPercentDict[ticker]
		returnsDict = returnPercentDict[ticker]
		filteredReturns = []
		for premarket, returnPercent in zip(premarketDict, returnsDict):
			if abs(premarket * 100) >= threshold:
				filteredReturns.append(returnPercent)
		thresholdReturnsDict[ticker].append(filteredReturns)

	while not thresholdReturnsDict[ticker][-1]:
		thresholdReturnsDict[ticker].pop(-1)

thresholds = [x / 100 for x in thresholds]

dolWeightedReturns = {}
avgPctReturns = {}
winPctsOnCloses = {}
avgPosPremarkPctReturns = {}
posPremarkWinPcts = {}
avgNegPremarkPctReturns = {}
negPremarkWinPcts = {}
maxPercentRets = {}

for ticker, returnList in returnPercentDict.items():
	fig, ax = plt.subplots(2, 3, figsize=(19, 8))
	print(ticker)
	dollarWeightedReturn = round(decimal.Decimal(reduce(operator.mul, returnList, 1)), DECIMAL_PLACES)
	print("Dollar-weighted return: " + str(dollarWeightedReturn))
	dolWeightedReturns[ticker] = dollarWeightedReturn
	# print("Dollar-weighted return excluding losses: " + str(round(decimal.Decimal(reduce(operator.mul, map(lambda x : max(x, 1), returnList), 1)), DECIMAL_PLACES)))
	avgPctReturn = round(decimal.Decimal(sum(returnList) / len(returnList)), DECIMAL_PLACES)
	print("Average percent return: " + str(avgPctReturn))
	avgPctReturns[ticker] = avgPctReturn
	winPctOnCloses = round(decimal.Decimal(sum(1 for i in returnList if i >= 1) / len(returnList) * 100), DECIMAL_PLACES)
	print("Win percent on closes: " + str(winPctOnCloses))
	winPctsOnCloses[ticker] = winPctOnCloses
	posPremarketReturns = [x for idx, x in enumerate(returnList) if premarketPercentDict[ticker][idx] >= 0]
	avgPosPremarkPctReturn = round(decimal.Decimal(sum(posPremarketReturns) / len(posPremarketReturns)), DECIMAL_PLACES)
	print("Average percent return for positive premarkets: " + str(avgPosPremarkPctReturn))
	avgPosPremarkPctReturns[ticker] = avgPosPremarkPctReturn
	posPremarkWinPct = round(decimal.Decimal(sum(1 for i in posPremarketReturns if i >= 1) / len(posPremarketReturns) * 100), DECIMAL_PLACES)
	print("Win percent on closes for positive premarkets: " + str(posPremarkWinPct))
	posPremarkWinPcts[ticker] = posPremarkWinPct
	negPremarketReturns = [x for idx, x in enumerate(returnList) if premarketPercentDict[ticker][idx] < 0]
	avgNegPremarkPctReturn = round(decimal.Decimal(sum(negPremarketReturns) / len(negPremarketReturns)), DECIMAL_PLACES)
	print("Average percent return for negative premarkets: " + str(avgNegPremarkPctReturn))
	avgNegPremarkPctReturns[ticker] = avgNegPremarkPctReturn
	negPremarkWinPct = round(decimal.Decimal(sum(1 for i in negPremarketReturns if i >= 1) / len(negPremarketReturns) * 100), DECIMAL_PLACES)
	print("Win percent on closes for negative premarkets: " + str(negPremarkWinPct))
	negPremarkWinPcts[ticker] = negPremarkWinPct
	minIndex = np.where(returnList == np.min(returnList))[0]
	print("Min percent return on closes: " + str(round(decimal.Decimal(min(returnList)), DECIMAL_PLACES)) + " on " + concatDates(minIndex, datesDict[ticker]))
	maxIndex = np.where(returnList == np.max(returnList))[0]
	maxPercentRet = round(decimal.Decimal(max(returnList)), DECIMAL_PLACES)
	print("Max percent return on closes: " + str(maxPercentRet) + " on " + concatDates(maxIndex, datesDict[ticker]))
	print()
	maxPercentRets[ticker] = maxPercentRet
	maxList = maxPercentDict[ticker]
	# print("Max dollar-weighted return: " + str(round(decimal.Decimal(reduce(operator.mul, maxList, 1)), DECIMAL_PLACES)))
	# print("Average max percent return: " + str(round(decimal.Decimal(sum(maxList) / len(maxList)), DECIMAL_PLACES)))
	# minIndex = np.where(maxList == np.min(maxList))[0]
	# print("Min max percent return: " + str(round(decimal.Decimal(min(maxList)), DECIMAL_PLACES)) + " on " + concatDates(minIndex, datesDict[ticker]))
	# maxIndex = np.where(maxList == np.max(maxList))[0]
	# print("Max max percent return: " + str(round(decimal.Decimal(max(maxList)), DECIMAL_PLACES)) + " on " + concatDates(maxIndex, datesDict[ticker]))

	counts, bins, patches = ax[0][0].hist(returnList, edgecolor='black')
	ax[0][0].set_title("Total returns")
	ax[0][0].set_xticks(bins)
	ax[0][0].xaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
	ax[0][0].tick_params(axis='x', labelsize=8)
	bin_centers = 0.5 * np.diff(bins) + bins[:-1]
	for count, x in zip(counts, bin_centers):
		ax[0][0].annotate(int(count), xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -18), textcoords='offset points', va='top', ha='center')
		percent = '{:.1%}'.format(float(count) / counts.sum())
		ax[0][0].annotate(percent, xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -28), textcoords='offset points', va='top', ha='center')

	counts, bins, patches = ax[0][1].hist(maxList, edgecolor='black')
	ax[0][1].set_title("Max percent returns")
	ax[0][1].set_xticks(bins)
	ax[0][1].xaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
	ax[0][1].tick_params(axis='x', labelsize=8)
	bin_centers = 0.5 * np.diff(bins) + bins[:-1]
	for count, x in zip(counts, bin_centers):
		ax[0][1].annotate(int(count), xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -18), textcoords='offset points', va='top', ha='center')
		percent = '{:.1%}'.format(float(count) / counts.sum())
		ax[0][1].annotate(percent, xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -28), textcoords='offset points', va='top', ha='center')

	counts, bins, patches = ax[0][2].hist(premarketPercentDict[ticker], edgecolor='black')
	ax[0][2].set_title("Premarket percents")
	ax[0][2].set_xticks(bins)
	ax[0][2].xaxis.set_major_formatter(FormatStrFormatter('%0.2f%%'))
	ax[0][2].tick_params(axis='x', labelsize=8)
	bin_centers = 0.5 * np.diff(bins) + bins[:-1]
	for count, x in zip(counts, bin_centers):
		ax[0][2].annotate(int(count), xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -18), textcoords='offset points', va='top', ha='center')
		percent = '{:.1%}'.format(float(count) / counts.sum())
		ax[0][2].annotate(percent, xy=(x, 0), fontsize=8, xycoords=('data', 'axes fraction'), xytext=(0, -28), textcoords='offset points', va='top', ha='center')

	# thresholdReturnsDict[ticker] = [ele for ele in thresholdReturnsDict[ticker] if ele != []]
	nonemptyThresholds = len(thresholdReturnsDict[ticker])
	totalReturns = list(map(lambda x : reduce(operator.mul, x, 1), thresholdReturnsDict[ticker]))
	ax[1][0].plot(thresholds[0:nonemptyThresholds], totalReturns)
	ax[1][0].set_title("Total return versus premarket threshold")
	ax[1][0].xaxis.set_major_formatter(FormatStrFormatter('%0.2f%%'))
	ax[1][0].tick_params(axis='x', labelsize=8)
	ax[1][0].set_xticks(np.linspace(min(thresholds[0:nonemptyThresholds]), max(thresholds[0:nonemptyThresholds]), min(12, nonemptyThresholds)))
	ax[1][0].grid(True, linestyle='--')

	winRates = list(map(lambda x : sum(1 for i in x if i >= 1) / len(x) * 100, thresholdReturnsDict[ticker]))
	ax[1][1].plot(thresholds[0:nonemptyThresholds], winRates)
	ax[1][1].set_title("Win rate versus premarket threshold")
	ax[1][1].xaxis.set_major_formatter(FormatStrFormatter('%0.2f%%'))
	ax[1][1].yaxis.set_major_formatter(FormatStrFormatter('%d%%'))
	ax[1][1].tick_params(axis='x', labelsize=8)
	ax[1][1].set_xticks(np.linspace(min(thresholds[0:nonemptyThresholds]), max(thresholds[0:nonemptyThresholds]), min(12, nonemptyThresholds)))
	ax[1][1].grid(True, linestyle='--')

	averageReturns = list(map(lambda x : sum(x) / len(x), thresholdReturnsDict[ticker]))
	ax[1][2].plot(thresholds[0:nonemptyThresholds], averageReturns)
	ax[1][2].set_title("Average return versus premarket threshold")
	ax[1][2].xaxis.set_major_formatter(FormatStrFormatter('%0.2f%%'))
	ax[1][2].tick_params(axis='x', labelsize=8)
	ax[1][2].set_xticks(np.linspace(min(thresholds[0:nonemptyThresholds]), max(thresholds[0:nonemptyThresholds]), min(12, nonemptyThresholds)))
	ax[1][2].grid(True, linestyle='--')

	plt.subplots_adjust(left=0.03,
		bottom=0.05,
		right=0.97,
		top=0.9,
		wspace=0.1,
		hspace=0.3)
	plt.suptitle(ticker[:-1])

print("SUMMARY")
print("Max dollar-weighted return: " + max(dolWeightedReturns, key=dolWeightedReturns.get) + " " + str(max(dolWeightedReturns.values())))
print("Max average percent return: " + max(avgPctReturns, key=avgPctReturns.get) + " " + str(max(avgPctReturns.values())))
print("Max win percent on closes: " + max(winPctsOnCloses, key=winPctsOnCloses.get) + " " + str(max(winPctsOnCloses.values())))
print("Max average positive premarket percent return: " + max(avgPosPremarkPctReturns, key=avgPosPremarkPctReturns.get) + " " + str(max(avgPosPremarkPctReturns.values())))
print("Max positive premarket win percent: " + max(posPremarkWinPcts, key=posPremarkWinPcts.get) + " " + str(max(posPremarkWinPcts.values())))
print("Max average negative premarket percent return: " + max(avgNegPremarkPctReturns, key=avgNegPremarkPctReturns.get) + " " + str(max(avgNegPremarkPctReturns.values())))
print("Max negative premarket win percent: " + max(negPremarkWinPcts, key=negPremarkWinPcts.get) + " " + str(max(negPremarkWinPcts.values())))
print("Max maximum percent return: " + max(maxPercentRets, key=maxPercentRets.get) + " " + str(max(maxPercentRets.values())))
plt.show()
