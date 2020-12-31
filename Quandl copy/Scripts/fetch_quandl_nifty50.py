import requests
import time
import csv

# import pandas as pd

#### Read codes Nifty50
nifty = open("../Codes/Nifty50", "r")
nifty_codes = []

for x in nifty:
    nifty_codes.append(x.rstrip("\n"))

nifty.close()

codes = nifty_codes

#### FETCH and SAVE data
API_KEY = "mqWP8oMDGMWDagBGa7Da"
PARAMS = {'api_key': API_KEY}

print("Total codes found: " + str(len(codes)))

end_date = "2020-12-24" # automate this

i=0
nReq_count = 0
start = time.time()
for x in codes:
    print("Number of codes fetched: " + str(i) + "/" + str(len(codes)) + ", currently fetching: " + x, end=" ", flush=False)
    URL = "https://www.quandl.com/api/v3/datasets/BSE/" + x + "/data.json"
    r = requests.get(url = URL, params = PARAMS)
    if r:
        data = r.json()

        not_required = False
        if data["dataset_data"]["end_date"] != end_date:
            not_required = True
            nReq_count = nReq_count + 1
        else:
            column_names = data["dataset_data"]["column_names"]

            data_rev = data["dataset_data"]["data"]
            data_rev.reverse()

            # For CSV
            with open("../Data/Nifty50/" + x + ".csv", "a+") as old_data:
                writer = csv.writer(old_data)
                writer.writerows(data_rev)
            del writer
            del old_data

            # For Excel
            # df = pd.DataFrame(data_rev, columns=column_names)
            # df.to_excel("Data/" + x + ".xls") # Saving to Excel
            # del df

            del data_rev
            del column_names
        del data
    else:
        print("<-- Data not received", end="\n", flush=False)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds), end=" ", flush=False)
    if not_required:
        print("<-- Data till current date not present on BSE", end="", flush=False)
    print(end="\n\r", flush=False)

    del URL
    del r
    i = i+1
print("\n")
print(str(len(codes)) + " codes processed.\n" + str(nReq_count) + " codes are obsolote.\n" + "Data for " + str(len(codes) - nReq_count) + " codes saved sucessfully.\n")
