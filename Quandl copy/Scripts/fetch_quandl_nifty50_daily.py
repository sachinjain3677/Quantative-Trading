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
API_KEY = "mqWP8oMDGMWDagBGa7Da"
Date = "2020-12-28"
PARAMS = {'start_date': Date, 'end_date': Date, 'api_key': API_KEY}

i=0
start = time.time()
for x in codes:
    print("Number of codes fetched: " + str(i) + "/" + str(len(codes)) + ", currently fetching: " + x, end=" ", flush=False)
    URL = "https://www.quandl.com/api/v3/datasets/BSE/" + x
    r = requests.get(url = URL, params = PARAMS)
    if r:
        data = r.json()

        not_updated = False
        if len(data["dataset"]["data"]) == 0:
            not_updated = True
        else:
            column_names = data["dataset"]["column_names"]

            # For CSV
            with open("../Data/Nifty50/" + x + ".csv", "a+") as old_data:
                writer = csv.writer(old_data)
                writer.writerows(data["dataset"]["data"])
            del writer
            del old_data

            #For Excel
            # df = pd.read_excel("../Data/Nifty50/" + x + ".xls")
            #
            # df_new = pd.DataFrame(data["dataset"]["data"], columns=column_names)
            # df = df.drop(["Unnamed: 0"], axis=1).append(df_new, ignore_index=True)
            #
            # df.to_excel("Data/" + x + ".xls")
            # del df
            # del df_new
            
            del column_names
        del data
    else:
        print("<-- Data not received", end="\n", flush=False)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds), end=" ", flush=False)
    print("<-- Data not updated on Quandl yet. Wait till 9:30am IST.", end="\n\r", flush=False)


    del URL
    del r
    i = i+1
