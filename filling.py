import numpy as np
import pandas as pd

df = pd.read_csv("data/Evolutionary Grounds Transactional Data.csv")
curr = 1
for i in range(len(df) - 4):
  if pd.isna(df.iloc[i]["Date"]):
    df.loc[i, "Date"] = curr
  elif df.iloc[i]["Date"] != "---":
    curr = df.iloc[i]["Date"]
    print(curr)
df.to_csv("Evolutionary Grounds Transactional Data.csv", index=False)