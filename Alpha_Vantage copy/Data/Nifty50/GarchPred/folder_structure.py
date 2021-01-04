import os
from shutil import copyfile
import pandas as pd

models = ["sGARCH", "gjrGARCH", "eGARCH"]
dists = ["norm", "std", "ged", "snorm", "sstd", "sged"]
for i in range(0,50):
    os.mkdir("./" + str(i))

best_models = pd.read_csv("./best_models.csv", header = 0, names=["Company Name", "Best Model", "Best Distribution", "Economic Significance"])

# print(best_models.loc[0]["Company Name"])

for i in range(0,26):
    best_model = best_models.loc[i]["Best Model"]
    best_dist = best_models.loc[i]["Best Distribution"]
    print("Company: " + str(i))
    print("Model: " + best_model)
    print("Dist: " + best_dist)
    print("Copying... " + "../bestModel/" + str(i) + "/" + best_model + "/" + best_model + "_" + best_dist + ".csv")
    copyfile("../bestModel/" + str(i) + "/" + best_model + "/" + best_model + "_" + best_dist + ".csv", "./" + str(i) + "/predictions.csv")
