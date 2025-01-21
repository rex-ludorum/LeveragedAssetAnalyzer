import json
import os

TICKER_LIST = ["SOXX/", "SOXL/", "SOXS/", "QQQ/", "TQQQ/", "SQQQ/", "FNGS/", "FNGU/", "FNGD/", "SPY/", "SPXL/", "SPXS/", "XLF/", "FAS/",
	"FAZ/", "VGT/", "TECL/", "TECS/", "VTWO/", "TNA/", "TZA/", "XBI/", "LABU/", "LABD/", "TLT/", "TMF/", "TMV/", "DIA/", "UDOW/",
	"SDOW/", "FXI/", "YINN/", "YANG/", "FDN/", "WEBL/", "WEBS/", "EEM/", "EDC/", "EDZ/", "SPHB/", "HIBL/", "HIBS/", "IYR/", "DRN/",
	"DRV/", "MDY/", "UMDD/", "SMDD/", "IEF/", "TYD/", "TYO/", "BNKU/", "BNKD/", "BULZ/", "BERZ/", "GDX/", "GDXJ/", "GDXU/", "GDXD/",
	"XLE/", "NRGU/", "NRGD/", "IEO/", "OILU/", "OILD/"]

for ticker in TICKER_LIST:
	masterJson = {}
	fileList = os.listdir(ticker)
	for file in fileList:
		with open(ticker + file, "r") as fileReader:
			data = json.load(fileReader)
			del data['status']
			del data['symbol']
			date = data.pop('from')
			masterJson[date] = data
	with open("data/" + ticker[:-1], "w") as fileWriter:
		fileWriter.write(json.dumps(masterJson, indent=2))
