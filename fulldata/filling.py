import numpy as np
import pandas as pd

csv_names = [
  "By_George_Sales",
  "Evolutionary Grounds Transactional Data",
  "Husky_Grind_March_Sales",
  "Mary_Gates_Transactional_Data",
  "Microsoft_Transactional_Data",
  "Orins_Sales"
  "Overpass Transactional Data"
  "Parnassus_Transactional_Data"
]
for name in csv_names:
  df = pd.read_csv("../data/"+ name +".csv")
  curr = 1
  for i in range(len(df) - 4):
    if pd.isna(df.iloc[i]["Date"]):
      df.loc[i, "Date"] = curr
    elif df.iloc[i]["Date"] != "---":
      curr = df.iloc[i]["Date"]
    if df.iloc[i]["Table Type"] == "Tab":
      df.loc[i, "Day Part"] = df.iloc[i - 1]["Day Part"]
  df.to_csv(name+".csv", index=False)