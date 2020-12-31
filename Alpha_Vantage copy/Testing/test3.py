import csv
import requests

API_KEY = "mqWP8oMDGMWDagBGa7Da"
PARAMS = {'api_key': API_KEY}
x = "BOM570001"
URL = "https://www.quandl.com/api/v3/datasets/BSE/" + x + "/data.json"
r = requests.get(url = URL, params = PARAMS)

data = r.json()

data_rev = data["dataset_data"]["data"]
data_rev.reverse()

print(data_rev)
# For CSV
# with open(x+".csv", "a+") as old_data:
#     writer = csv.writer(old_data)
#     writer.writerows(data_rev)
# del writer
# del old_data
