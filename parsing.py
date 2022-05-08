import numpy as np
import pandas as pd

weekdays = {0: "Mon", 1:"Tue", 2:"Wed", 3:"Thu", 4: "Fri", 5: "Sat", 6:"Sun"} # remember to % 7
times = [
  "07:00", "07:15", "07:30", "07:45",
  "08:00", "08:15", "08:30", "08:45",
  "09:00", "09:15", "09:30", "09:45",
  "10:00", "10:15", "10:30", "10:45",
  "11:00", "11:15", "11:30", "11:45",
  "12:00", "12:15", "12:30", "12:45",
  "13:00", "13:15", "13:30", "13:45",
  "14:00", "14:15", "14:30", "14:45",
  "15:00", "15:15", "15:30", "15:45",
  "16:00", "16:15", "16:30", "16:45",
  "17:00", "17:15", "17:30", "17:45",
  "18:00", "18:15", "18:30", "18:45"
  ]

"""
Relevant Info to Parse:
  Day of the week
  Time period
  # transactions (seems to be equivalent to guests/tables)
"""
def parsedData():
  eg = pd.read_csv("fulldata/Evolutionary Grounds Transactional Data.csv")
  eg_sum = np.zeros((len(times), 7))
  for i in range(len(eg)):
    slice = eg.iloc[i]
    if slice["Day Part"] != "---":
      eg_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]

  hg = pd.read_csv("fulldata/Husky_Grind_March_Sales.csv")
  hg_sum = np.zeros((len(times), 7))
  for i in range(len(hg)):
    slice = hg.iloc[i]
    if slice["Day Part"] != "---" and slice["Net Sales"] > 0:
      hg_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]

  mg = pd.read_csv("fulldata/Mary_Gates_Transactional_Data.csv")
  mg_sum = np.zeros((len(times), 7))
  for i in range(len(mg)):
    slice = mg.iloc[i]
    if slice["Day Part"] != "---":
      mg_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]

  mc = pd.read_csv("fulldata/Microsoft_Transactional_Data.csv")
  mc_sum = np.zeros((len(times), 7))
  for i in range(len(mc)):
    slice = mc.iloc[i]
    if slice["Day Part"] != "---":
      mc_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]

  op = pd.read_csv("fulldata/Overpass Transactional Data.csv")
  op_sum = np.zeros((len(times), 7))
  for i in range(len(op)):
    slice = op.iloc[i]
    if slice["Day Part"] != "---":
      op_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]

  pn = pd.read_csv("fulldata/Parnassus_Transactional_Data.csv")
  pn_sum = np.zeros((len(times), 7))
  for i in range(len(pn)):
    slice = pn.iloc[i]
    if slice["Day Part"] != "---":
      pn_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]
  res = {}
  for day in range(0,7):
    data = {
      "Timeslot": times,
      "Evolutionary Grounds": eg_sum[:, day],
      "Husky Grind": hg_sum[:, day],
      "Mary Gates": mg_sum[:, day],
      "Microsoft Cafe": mc_sum[:, day],
      "Overpass": op_sum[:, day],
      "Parnassus": pn_sum[:, day]
      }
    res[weekdays[day]] = pd.DataFrame(data)
  return res

if __name__ == "__main__":
  print(parsedData())