import requests
import json
requests.packages.urllib3.disable_warnings()
import pandas as pd
from jdatetime import date, timedelta

d1 = date(1402,2,1)
d2 = date(1402,2,14)
delta = (d2 - d1).days
date_list = []
for i in range(delta + 1):
    day = d1 + timedelta(days=i)
    day = day.strftime("%Y-%m-%d")
    date_list.append(day)

data_frame = pd.DataFrame()
for date in date_list:
    airline = 'irm'
    url = f'https://ais.airport.ir/NetForm/Service/fids?date={date}&airline={airline}&AUTH_TOKEN=7012367'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    response = requests.get(url,headers=headers,verify = False)
    d = json.loads(response.text)
    data=d["Flights"]
    for key in data:
        print(key)
        key["Airline"]= airline
        key["Date"]= date
    data = pd.DataFrame(data)
    data_frame = pd.concat([data_frame, data], axis=0)
  
data_frame.to_csv('Farbod_orang1.csv', index=False)