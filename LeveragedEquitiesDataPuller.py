import requests
import datetime
import json
import os
import time
from dateutil import relativedelta
from requests.compat import urljoin

todayDate = datetime.datetime.now().date()
#iterDate = todayDate - relativedelta.relativedelta(years=2)
iterDate = datetime.datetime.strptime("2021-02-24", "%Y-%m-%d").date()

baseUrl = "https://api.polygon.io/v1/open-close/"

#tickerList = ["SOXX/", "SOXL/", "SOXS/", "QQQ/", "TQQQ/", "SQQQ/", "FNGS/", "FNGU/", "FNGD/"]
tickerList = ["SPY/", "SPXL/", "SPXS/", "XLF/", "FAS/", "FAZ/", "VGT/", "TECL/", "TECS/", "VTWO/", "TNA/", "TZA/", "XBI/", "LABU/",
    "LABD/", "TLT/", "TMF/", "TMV/", "DIA/", "UDOW/", "SDOW/", "FXI/", "YINN/", "YANG/", "FDN/", "WEBL/", "WEBS/", "EEM/", "EDC/",
    "EDZ/", "SPHB/", "HIBL/", "HIBS/", "IYR/", "DRN/", "DRV/", "MDY/", "UMDD/", "SMDD/", "IEF/", "TYD/", "TYO/", "BNKU/", "BNKD/",
    "BULZ/", "BERZ/", "GDX/", "GDXJ/", "GDXU/", "GDXD/", "XLE/", "NRGU/", "NRGD/", "IEO/", "OILU/", "OILD/"]

for ticker in tickerList:
    os.makedirs(ticker, exist_ok=True)

params = {
    'apiKey': 'YOUR_API_KEY',
    'adjusted': 'true'
}

while iterDate < todayDate:
    for ticker in tickerList:
        if (ticker == "BULZ/" or ticker == "BERZ/") and iterDate.strftime('%Y-%m-%d') < "2021-08-18":
            continue
        if (ticker == "OILU/" or ticker == "OILD/" or ticker == "IEO/") and iterDate.strftime('%Y-%m-%d') < "2021-11-09":
            continue
        specificUrl = urljoin(baseUrl, ticker)
        if iterDate.isoweekday() in set((6, 7)):
            iterDate += relativedelta.relativedelta(days=8 - iterDate.isoweekday())
        specificUrl = urljoin(specificUrl, iterDate.strftime('%Y-%m-%d'))
        response = requests.get(specificUrl, params=params)
        if response.ok:
            json_object = json.dumps(response.json(), indent=4)
            with open(ticker + iterDate.strftime('%Y-%m-%d'), "w") as fileWriter:
                fileWriter.write(json_object)
        time.sleep(12.2)
    iterDate += relativedelta.relativedelta(days=1)