import requests
import time
import csv

# import pandas as pd

#### Read codes
nifty = open("../Codes/Nifty50", "r")
nifty_codes = []

for x in nifty:
    nifty_codes.append(x.rstrip("\n"))

nifty.close()

codes = nifty_codes

#### FETCH and SAVE data
URL = "https://www.alphavantage.co/query?"
function = "TIME_SERIES_DAILY_ADJUSTED"
apikey = "4KCLG1SNH4PB6P2J"
datatype = "csv"
outputsize = "compact"

PARAMS = {'function': function, 'apikey': apikey, 'datatype':datatype, 'outputsize': outputsize, 'symbol': codes[0]}
r = requests.get(url = URL, params = PARAMS)

data = r.text
data = data.split("\n")
data = [row.strip() for row in data]
data = list(filter(len, data))
column_names = data[0].split(",")
data = data[1:]
data.reverse()
# print(data)
idx_timestamp = column_names.index("timestamp")
idx_adjClose = column_names.index("adjusted_close")

print(idx_timestamp)
print(idx_adjClose)

data = [x.split(",") for x in data]
data = [[x[idx_timestamp], x[idx_adjClose]] for x in data]

print(data)
# print(len(data))
# print(column_names)
# with open("sample.csv", "a+") as old_data:
#     writer = csv.writer(old_data)
#     writer.writerows(data)
