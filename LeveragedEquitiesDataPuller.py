import requests
import datetime
import json
import os
import time
from dateutil import relativedelta
from requests.compat import urljoin

todayDate = datetime.datetime.now().date()
iterDate = todayDate - relativedelta.relativedelta(years=2)

baseUrl = "https://api.polygon.io/v1/open-close/"

tickerList = ["SOXX/", "SOXL/", "SOXS/", "QQQ/", "TQQQ/", "SQQQ/", "FNGS/", "FNGD/", "FNGU/"]

params = {
    'apiKey': 'YOUR_API_KEY',
    'adjusted': 'true'
}

for ticker in tickerList:
    specificUrl = urljoin(baseUrl, ticker)
    while iterDate < todayDate:
        if iterDate.isoweekday() in set((6, 7)):
            iterDate += relativedelta.relativedelta(days=8 - iterDate.isoweekday())
        specificUrl = urljoin(specificUrl, iterDate.strftime('%Y-%m-%d'))
        response = requests.get(specificUrl, params=params)
        if response.ok:
            json_object = json.dumps(response.json(), indent=4)
            os.makedirs(ticker, exist_ok=True)
            with open(ticker + iterDate.strftime('%Y-%m-%d'), "w") as fileWriter:
                fileWriter.write(json_object)
        iterDate += relativedelta.relativedelta(days=1)
        time.sleep(12.5)