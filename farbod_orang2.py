import mysql.connector as mysql
import requests
import json
requests.packages.urllib3.disable_warnings()
from jdatetime import date, timedelta

conn = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "asddsa",
    database = "fids_2"
)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS FIDS (
    origin NVARCHAR(250),destination NVARCHAR(250),scheduled_time NVARCHAR(250),scheduled_date NVARCHAR(250),
    destination_icao NVARCHAR(250),dow NVARCHAR(250),flight_num NVARCHAR(250),actual_date NVARCHAR(250),
    origin_icao NVARCHAR(250),airline_icao NVARCHAR(250),airline NVARCHAR(250),international BIT,
    airplane_type NVARCHAR(250),miladi_scheduled DATE,actual_time NVARCHAR(250),delay INT,
    miladi_actual DATE,type_ NVARCHAR(250),Date_ NVARCHAR(250)
    )""")

d1 = date(1402,2,1)
d2 = date(1402,2,14)
AUTH_TOKEN = 7012367

airlines = ["IRA","IRB","IRC","IZG","IRK","IRQ","IRM","TBZ","MRJ","TBM","CPN","IRG","SHI","VRH"]
for airline in airlines:
    delta = (d2 - d1).days
    date_list = []
    for i in range(delta + 1):
        day = d1 + timedelta(days=i)
        day = day.strftime("%Y-%m-%d")
        date_list.append(day)

    for date in date_list:
        url = f'https://ais.airport.ir/NetForm/Service/fids?date={date}&airline={airline}&AUTH_TOKEN={AUTH_TOKEN}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
                "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate"}
        response = requests.get(url,headers=headers,verify = False)
        data = json.loads(response.text)
        flights = data["Flights"]
        for key in flights:
            values = []
            items = ["origin","destination","scheduled_time","scheduled_time","destination_icao","dow","flight_num","actual_date","origin_icao",
            "airline_icao","airline","international","airplane_type","miladi_scheduled","actual_time","delay","miladi_actual","type_"]
            for i in items:
                if i == "international":
                    data = 0 if key[i]== "false" else 1
                elif i == "delay":
                    data= 0 if key[i] == 'NULL' else key[i]
                else:
                    data = key[i]
                values.append(data)
            values = tuple(values)
            sql = """insert into FIDS(origin,destination,scheduled_time,scheduled_date,destination_icao,dow,flight_num,actual_date,origin_icao,airline_icao,
                    airline,international,airplane_type,miladi_scheduled,actual_time,delay,miladi_actual,type_) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            try:
                cursor.execute(sql,values)
                conn.commit()
            except mysql.Error as error:
                print(error)
    N_delays = {}
    sql = '''SELECT * From fids'''
    cursor.execute(sql)
    recs = cursor.fetchall()
    for row in recs:
        dow = row[5]
        delay = row[15]
        if delay>0:
            try:
                N_delays[dow] += 1
            except:
                N_delays[dow] = 1

    for i in N_delays:
        print(f"{i}:{N_delays[i]}")

