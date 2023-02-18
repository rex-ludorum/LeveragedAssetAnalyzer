import requests
import datetime
from dateutil import relativedelta
from requests.compat import urljoin

todayDate = datetime.datetime.now().date()
iterDate = todayDate - relativedelta.relativedelta(years=2)
if iterDate.isoweekday() in set((6, 7)):
    iterDate += relativedelta.relativedelta(days=8 - iterDate.isoweekday())

while iterDate < todayDate:
    iterDate += relativedelta.relativedelta(days=1)
    if iterDate.isoweekday() in set((6, 7)):
        iterDate += relativedelta.relativedelta(days=8 - iterDate.isoweekday())
    print(iterDate)

baseUrl = "https://api.polygon.io/v1/open-close/"

tickerList = ["SOXX/", "SOXL/", "SOXS/", "QQQ/", "TQQQ/", "SQQQ/", "FNGS/", "FNGD/", "FNGU/"]

params = {
    'apiKey': 'YOUR_API_KEY_HERE',
    'adjusted': 'true'
}

for ticker in tickerList:
    specificUrl = urljoin(baseUrl, ticker)

ticker = "SOXX/"
date = "2021-02-17"
specificUrl = urljoin(baseUrl, ticker)
specificUrl = urljoin(specificUrl, date)

mlkDay2022 = datetime.datetime(2022, 1, 18)
specificUrl = urljoin(baseUrl, ticker)
specificUrl = urljoin(specificUrl, mlkDay2022.strftime('%Y-%m-%d'))
print(specificUrl)

response = requests.get(specificUrl, params=params)
print(response.json())