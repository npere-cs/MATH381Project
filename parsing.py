import numpy as np
import pandas as pd

weekdays = {0: "Mon", 1:"Tue", 2:"Wed", 3:"Thu", 4: "Fri", 5: "Sat", 6:"Sun"} # remember to % 7
staff_times = [
  "06:30", "06:45",
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
  "18:00", "18:15", "18:30"
]
times = staff_times[2:47]

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
  for day in range(7):
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

"""

"""
def parsedSums():
  eg = pd.read_csv("fulldata/Evolutionary Grounds Transactional Data.csv")
  eg = eg[eg["Day Part"] == "---"]
  eg_sum = np.zeros(7)
  for i in range(len(eg)):
    slice = eg.iloc[i]
    if slice["Date"] != "---":
      eg_sum[int(slice["Date"]) % 7] += slice["# Trans"]

  hg = pd.read_csv("fulldata/Husky_Grind_March_Sales.csv")
  hg = hg[hg["Day Part"] == "---"]
  hg_sum = np.zeros(7)
  for i in range(len(hg)):
    slice = hg.iloc[i]
    if slice["Date"] != "---":
      hg_sum[int(slice["Date"]) % 7] += slice["# Trans"]

  mg = pd.read_csv("fulldata/Mary_Gates_Transactional_Data.csv")
  mg = mg[mg["Day Part"] == "---"]
  mg_sum = np.zeros(7)
  for i in range(len(mg)):
    slice = mg.iloc[i]
    if slice["Date"] != "---":
      mg_sum[int(slice["Date"]) % 7] += slice["# Trans"]

  mc = pd.read_csv("fulldata/Microsoft_Transactional_Data.csv")
  mc = mc[mc["Day Part"] == "---"]
  mc_sum = np.zeros(7)
  for i in range(len(mc)):
    slice = mc.iloc[i]
    if slice["Date"] != "---":
      mc_sum[int(slice["Date"]) % 7] += slice["# Trans"]

  op = pd.read_csv("fulldata/Overpass Transactional Data.csv")
  op = op[op["Day Part"] == "---"]
  op_sum = np.zeros(7)
  for i in range(len(op)):
    slice = op.iloc[i]
    if slice["Date"] != "---":
      op_sum[int(slice["Date"]) % 7] += slice["# Trans"]

  pn = pd.read_csv("fulldata/Parnassus_Transactional_Data.csv")
  pn = pn[pn["Day Part"] == "---"]
  pn_sum = np.zeros(7)
  for i in range(len(pn)):
    slice = pn.iloc[i]
    if slice["Date"] != "---":
      pn_sum[int(slice["Date"]) % 7] += slice["# Trans"]

  print(eg_sum)
  print(hg_sum)
  print(mg_sum)
  print(mc_sum)
  print(op_sum)
  print(pn_sum)
  data = {
    "Day of the Week": weekdays.values(),
    "Evolutionary Grounds": eg_sum,
    "Husky Grind": hg_sum,
    "Mary Gates": mg_sum,
    "Microsoft Cafe": mc_sum,
    "Overpass": op_sum,
    "Parnassus": pn_sum
    }
  return pd.DataFrame(data)
"""
Does NOT account for By George or Orin's Place
"""
def parsedHours():
  hours = pd.read_csv("data/Location_Hours.csv")
  res = {}
  for day in range(7):
    df = pd.DataFrame({"Timeslot": times})
    for i in range(6): # Update this to len(df) later!
      location = hours["Location"].iloc[i]
      start = hours[str(weekdays[day])+"Open"].iloc[i]
      if start != "-":
        end = hours[str(weekdays[day])+"Close"].iloc[i]
        start_index = times.index(start)
        end_index = times.index(end)
        df[location] = [False] * start_index + [True] * (end_index - start_index) + [False] * (len(times) - end_index)
      else:
        df[location] = [False] * len(times)
    res[weekdays[day]] = df
  return res

"""
Does NOT account for By George or Orin's Place
"""
def parsedStaffing():
  hours = pd.read_csv("data/Location_Staffing_Hours.csv")
  res = {}
  for day in range(7):
    df = pd.DataFrame({"Timeslot": staff_times})
    for i in range(6): # Update this to len(df) later!
      location = hours["Location"].iloc[i]
      start = hours[str(weekdays[day])+"Open"].iloc[i]
      if start != "-":
        end = hours[str(weekdays[day])+"Close"].iloc[i]
        start_index = staff_times.index(start)
        end_index = staff_times.index(end)
        df[location] = [False] * start_index + [True] * (end_index - start_index) + [False] * (len(staff_times) - end_index)
      else:
        df[location] = [False] * len(staff_times)
    res[weekdays[day]] = df
  return res

if __name__ == "__main__":
  #print(parsedData())
  print(parsedSums())
  #print(parsedHours())
  #print(parsedStaffing())