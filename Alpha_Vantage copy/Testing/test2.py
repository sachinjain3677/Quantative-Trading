import pandas as pd

temp = pd.DataFrame(columns=["company name", "best model"])
for i in range(5):
    temp.loc[i] = [1,2]
    print(temp)
