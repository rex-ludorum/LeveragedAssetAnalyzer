import requests
import datetime
import json
import os
import time
import traceback
from dateutil import relativedelta
from requests.compat import urljoin

todayDate = datetime.datetime.now().date()
# iterDate = todayDate - relativedelta.relativedelta(years=2)
# date from which we are starting the collection
iterDate = datetime.datetime.strptime("2025-01-23", "%Y-%m-%d").date()

BASE_URL = "https://api.polygon.io/v1/open-close/"

TICKER_LIST = [
	"SOXX", "SOXL", "SOXS", "QQQ", "TQQQ", "SQQQ", "FNGS", "FNGU", "FNGD", "SPY", "SPXL", "SPXS", "XLF", "FAS",
	"FAZ", "VGT", "TECL", "TECS", "VTWO", "TNA", "TZA", "XBI", "LABU", "LABD", "TLT", "TMF", "TMV", "DIA", "UDOW",
	"SDOW", "FXI", "YINN", "YANG", "FDN", "WEBL", "WEBS", "EEM", "EDC", "EDZ", "SPHB", "HIBL", "HIBS", "IYR", "DRN",
	"DRV", "MDY", "UMDD", "SMDD", "IEF", "TYD", "TYO", "BULZ", "BERZ", "GDX", "GDXJ", "GDXU", "GDXD", "XLE", "IEO",
	"OILU", "OILD"
]

POLYGON_API_KEY = os.environ.get("POLYGON_API_KEY")

# os.makedirs(ticker, exist_ok=True)

params = {
	'apiKey': POLYGON_API_KEY,
	'adjusted': 'true',
}

while iterDate < todayDate:
	for ticker in TICKER_LIST:
		if (ticker == "BULZ" or ticker == "BERZ") and iterDate.strftime('%Y-%m-%d') < "2021-08-18":
			continue
		if (ticker == "OILU" or ticker == "OILD") and iterDate.strftime('%Y-%m-%d') < "2021-11-09":
			continue
		if (ticker == "IEO") and iterDate.strftime('%Y-%m-%d') < "2021-11-08":
			continue
		specificUrl = urljoin(BASE_URL, ticker)
		if iterDate.isoweekday() in set((6, 7)):
			iterDate += relativedelta.relativedelta(days=8-iterDate.isoweekday())

		dateString = iterDate.strftime('%Y-%m-%d')

		with open('data/' + ticker, "r") as fileReader:
			masterJson = json.load(fileReader)
			if dateString in masterJson:
				print(ticker + " already has data for " + dateString + ", skipping")
				continue

		specificUrl = urljoin(specificUrl, dateString)
		try:
			print("Sending request for " + specificUrl)
			response = requests.get(specificUrl, params=params)
			response.raise_for_status()
			data = response.json()
			if data['status'] != "OK":
				print("Unknown status: " + data['status'])
			# json_object = json.dumps(response.json(), indent=2)
			# with open(ticker + iterDate.strftime('%Y-%m-%d'), "w") as fileWriter:
				# fileWriter.write(json_object)
			del data['status']
			del data['symbol']
			date = data.pop('from')
			# print(json_object)
			masterJson = {}
			with open("data/" + ticker, "r") as fileReader:
				masterJson = json.load(fileReader)
			if not masterJson:
				print("Error reading data/" + ticker)
				continue
			masterJson[date] = data
			with open("data/" + ticker, "w") as fileWriter:
				fileWriter.write(json.dumps(masterJson, indent=2))
		except requests.HTTPError as e:
			print("Encountered HTTPError %s" % (repr(e)))
			traceback.print_exc()
		except Exception as e:
			print("Encountered other exception %s" % (repr(e)))
			traceback.print_exc()

		time.sleep(12.1)

	iterDate += relativedelta.relativedelta(days=1)
