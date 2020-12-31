import os

models = ["sGarch", "gjrGarch", "eGarch"]
dists = ["norm", "std", "ged", "snorm", "sstd", "sged"]
for i in range(2,50):
    # os.mkdir("./" + str(i))
    for j in models:
        # os.mkdir(str(i) + "/" + j)
        for k in dists:
            os.remove(str(i) + "/" + j + "/" + k)
