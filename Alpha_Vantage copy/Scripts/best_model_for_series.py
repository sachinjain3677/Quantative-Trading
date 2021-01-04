import pandas as pd
import numpy as np

models = ["sGARCH", "gjrGARCH", "eGARCH"]
dists = ["norm", "std", "ged", "snorm", "sstd", "sged"]

output = pd.DataFrame(columns=["Company Name", "Best Model", "Best Distribution", "Economic Significance"])
cnt=0
for one in range(0,41):
    print("Finding Best model for company name: " + str(one) + ". Total Companies = 50")
    file_path =  "../Data/old/" + str(one) + ".csv"

    data = pd.read_csv(file_path, header=None, names=["timestamp", "adjusted_close"])
    data = data[-27:].reset_index(drop = True)
    data_log = np.log(data["adjusted_close"].tolist())

    ret = []
    for i in range(1,27):
        ret.append(data_log[i] - data_log[i-1])

    data = data[1:]
    data["return"] = ret

    model_wise_return = []

    for two in models:
        for three in dists:
            data_this = data

            path = "../Data/Nifty50/bestModel/" + str(one) + "/" + two + "/" + two + "_" + three + ".csv"

            model_pred = pd.read_csv(path, names=["return_prediction", "volatility_prediction"], header=0)
            ret_pred = model_pred["return_prediction"][:26]

            data_this["return_prediction"] = ret_pred

            economic_sig = []
            for i in range(1,27):
                if data_this["return"][i] * data_this["return_prediction"][i] > 0:
                    economic_sig.append(abs(data_this["return"][i]))
                else:
                    economic_sig.append(-abs(data_this["return"][i]))

            data_this["economic_significance"] = economic_sig

            model_wise_return.append(data_this["economic_significance"].sum())

            del data_this
            del path
            del model_pred
            del ret_pred
            del economic_sig

    max_eco_sig = max(model_wise_return)
    max_return_idx = model_wise_return.index(max_eco_sig)

    best_model = int(max_return_idx/len(dists))
    best_dist = int(max_return_idx%len(dists))

    output.loc[cnt] = [one, models[best_model], dists[best_dist], max_eco_sig*100]
    cnt = cnt + 1
    print(output)
    print()
    print()

    del data
    del data_log
    del ret
    del model_wise_return
    del max_eco_sig
    del max_return_idx
    del best_model
    del best_dist

output.reset_index(drop=True)
output.to_csv("../Data/Nifty50/GarchPred/best_models.csv")
