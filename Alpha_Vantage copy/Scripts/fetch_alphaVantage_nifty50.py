import requests
import time
import csv
from datetime import datetime

# import pandas as pd

#### Read codes
nifty = open("../Codes/Nifty50", "r")
nifty_codes = []

for x in nifty:
    nifty_codes.append(x.rstrip("\n"))

nifty.close()

codes = nifty_codes

#### Read API Keys
apikeys = open("../Alpha_vantage_API_Key", "r")
api_keys = []

for x in apikeys:
    api_keys.append(x.rstrip("\n"))

apikeys.close()

#### Set parameters
function = "TIME_SERIES_DAILY_ADJUSTED"
key = 0
datatype = "csv"
outputsize = "full"

#### Start loop
i=0
start = time.time()
for x in codes:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    #### 5 calls per minute constraint walkthrough
    if i!=0 and i%5==0:
        print("Changing API Key...")
        key = (key + 1) % len(api_keys)
        print("Sleeping for " + str(60 - int(current_time[-2:]) + 2) + " seconds...\n")
        time.sleep(60 - int(current_time[-2:]) + 2)

    #### API call
    print("Fetching code number: " + str(i+1) + "/" + str(len(codes)) + ", currently fetching: " + x + ", using api key: " + api_keys[key], end=" ", flush=False)
    URL = "https://www.alphavantage.co/query?"
    PARAMS = {'function': function, 'apikey': api_keys[key], 'datatype':datatype, 'outputsize': outputsize, 'symbol': x}
    r = requests.get(url = URL, params = PARAMS)

    #### Call successful
    if "Error Message" not in r.text:
        #### Data preprocessing phase 1
        data = r.text
        data = data.split("\n")
        data = [row.strip() for row in data]
        data = list(filter(len, data))
        column_names = data[0].split(",")
        data = data[1:]

        #### Column test for "timestamp" and "adjusted_close"
        bool_timestamp = "timestamp" in column_names
        bool_adjClose = "adjusted_close" in column_names

        if bool_timestamp:
            idx_timestamp = column_names.index("timestamp")
        else:
            print("timestamp column doesn't exist in data", end=" ", flush=False)

        if bool_adjClose:
            idx_adjClose = column_names.index("adjusted_close")
        else:
            print("adjusted_close column doesn't exist in data", end=" ", flush=False)

        #### Check if relevant data exists
        empty = False
        if len(data) == 0 and (bool_timestamp or bool_adjClose):
            empty = True
        else:
            #### Data preprocessing phase 2
            data.reverse()
            data = [el.split(",") for el in data]
            data = [[el[idx_timestamp], el[idx_adjClose]] for el in data]


            #### Saving Data
            # For CSV
            with open("../Data/Nifty50/" + str(i) + ".csv", "a+") as old_data:
                writer = csv.writer(old_data)
                writer.writerows(data)
            del writer
            del old_data

            #For Excel
            # df = pd.DataFrame(data, columns=column_names)
            # df.to_excel("../Data/" + x + ".xls")
            # del df

            del column_names
        del data
    #### Call failed
    else:
        print("<-- Error Found. " + r.json()["Error Message"], end=" ", flush=False)

    #### Printing time taken for this ticker
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds), end=" ", flush=False)

    if empty:
        print("<-- Data not available on Alpha Vantage. Please check your request is correct.", end="", flush=False)

    print("", end="\n\r", flush=False)


    del URL
    del r
    i = i+1
