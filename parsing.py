import numpy as np
import pandas as pd

weekdays = {0: "Mon", 1:"Tue", 2:"Wed", 3:"Thu", 4: "Fri", 5: "Sat", 6:"Sun"}
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
times = staff_times[2:47] # location hours don't include setup or cleanup
locations = ["BG", "EG", "HG", "MG", "MS", "OP", "OV", "PS"]

"""
Returns dictionary where keys are each day of the week and values are DataFrames such that:
  Rows represent 15-minute timeslots
  Columns represent different locations
  Elements represent average transactions for one weekday, time, and location over all data
"""
def parsedData():
  bg = pd.read_csv("fulldata/By_George_Sales.csv")
  bg_sum = np.zeros((len(times), 7))
  bg_days = np.zeros(7)
  curr_day = 0
  for i in range(len(bg)):
    slice = bg.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      bg_days[int(curr_day) % 7] += 1
    if slice["Day Part"] != "---":
      bg_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]
  for timeslot in bg_sum:
    for day in range(7):
      if bg_days[day] > 1:
        timeslot[day] /= bg_days[day]

  eg = pd.read_csv("fulldata/Evolutionary Grounds Transactional Data.csv")
  eg_sum = np.zeros((len(times), 7))
  eg_days = np.zeros(7)
  curr_day = 0
  for i in range(len(eg)):
    slice = eg.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      eg_days[int(curr_day) % 7] += 1
    if slice["Day Part"] != "---":
      eg_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]
  for timeslot in eg_sum:
    for day in range(7):
      if eg_days[day] > 1:
        timeslot[day] /= eg_days[day]

  hg = pd.read_csv("fulldata/Husky_Grind_March_Sales.csv")
  hg_sum = np.zeros((len(times), 7))
  hg_days = np.zeros(7)
  curr_day = 0
  for i in range(len(hg)):
    slice = hg.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      hg_days[int(curr_day) % 7] += 1
    if slice["Day Part"] != "---" and slice["Net Sales"] > 0:
      hg_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]
  for timeslot in hg_sum:
    for day in range(7):
      if hg_days[day] > 1:
        timeslot[day] /= hg_days[day]

  mg = pd.read_csv("fulldata/Mary_Gates_Transactional_Data.csv")
  mg_sum = np.zeros((len(times), 7))
  mg_days = np.zeros(7)
  curr_day = 0
  for i in range(len(mg)):
    slice = mg.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      mg_days[int(curr_day) % 7] += 1
    if slice["Day Part"] != "---":
      mg_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]
  for timeslot in mg_sum:
    for day in range(7):
      if mg_days[day] > 1:
        timeslot[day] /= mg_days[day]

  ms = pd.read_csv("fulldata/Microsoft_Transactional_Data.csv")
  ms_sum = np.zeros((len(times), 7))
  ms_days = np.zeros(7)
  curr_day = 0
  for i in range(len(ms)):
    slice = ms.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      ms_days[int(curr_day) % 7] += 1
    if slice["Day Part"] != "---":
      ms_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]
  for timeslot in ms_sum:
    for day in range(7):
      if ms_days[day] > 1:
        timeslot[day] /= ms_days[day]

  op = pd.read_csv("fulldata/Orins_Sales.csv")
  op_sum = np.zeros((len(times), 7))
  op_days = np.zeros(7)
  curr_day = 0
  for i in range(len(op)):
    slice = op.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      op_days[int(curr_day) % 7] += 1
    if slice["Day Part"] != "---" and slice["Table Type"] == "---":
      op_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]
  for timeslot in op_sum:
    for day in range(7):
      if op_days[day] > 1:
        timeslot[day] /= op_days[day]

  ov = pd.read_csv("fulldata/Overpass Transactional Data.csv")
  ov_sum = np.zeros((len(times), 7))
  ov_days = np.zeros(7)
  curr_day = 0
  for i in range(len(ov)):
    slice = ov.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      ov_days[int(curr_day) % 7] += 1
    if slice["Day Part"] != "---":
      ov_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]
  for timeslot in ov_sum:
    for day in range(7):
      if ov_days[day] > 1:
        timeslot[day] /= ov_days[day]

  ps = pd.read_csv("fulldata/Parnassus_Transactional_Data.csv")
  ps_sum = np.zeros((len(times), 7))
  ps_days = np.zeros(7)
  curr_day = 0
  for i in range(len(ps)):
    slice = ps.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      ps_days[int(curr_day) % 7] += 1
    if slice["Day Part"] != "---":
      ps_sum[times.index((slice["Day Part"])[:5])][int(slice["Date"]) % 7] += slice["# Trans"]
  for timeslot in ps_sum:
    for day in range(7):
      if ps_days[day] > 1:
        timeslot[day] /= ps_days[day]

  res = {}
  for day in range(7):
    data = {
      "Timeslot": times,
      "BG": bg_sum[:, day],
      "EG": eg_sum[:, day],
      "HG": hg_sum[:, day],
      "MG": mg_sum[:, day],
      "MS": ms_sum[:, day],
      "OP": op_sum[:, day],
      "OV": ov_sum[:, day],
      "PS": ps_sum[:, day]
      }
    res[weekdays[day]] = pd.DataFrame(data)
  return res

"""
Returns DataFrame of average daily transactions over all locations and weekdays.
"""
def parsedTotals():
  bg = pd.read_csv("fulldata/By_George_Sales.csv")
  bg = bg[bg["Day Part"] == "---"]
  bg_sum = np.zeros(7)
  bg_days = np.zeros(7)
  curr_day = 0
  for i in range(len(bg)):
    slice = bg.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      bg_days[int(curr_day) % 7] += 1
    if slice["Date"] != "---":
      bg_sum[int(slice["Date"]) % 7] += slice["# Trans"]
  for day in range(7):
    if bg_days[day] > 1:
      bg_sum[day] /= bg_days[day]

  eg = pd.read_csv("fulldata/Evolutionary Grounds Transactional Data.csv")
  eg = eg[eg["Day Part"] == "---"]
  eg_sum = np.zeros(7)
  eg_days = np.zeros(7)
  curr_day = 0
  for i in range(len(eg)):
    slice = eg.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      eg_days[int(curr_day) % 7] += 1
    if slice["Date"] != "---":
      eg_sum[int(slice["Date"]) % 7] += slice["# Trans"]
  for day in range(7):
    if eg_days[day] > 1:
      eg_sum[day] /= eg_days[day]

  hg = pd.read_csv("fulldata/Husky_Grind_March_Sales.csv")
  hg = hg[hg["Day Part"] == "---"]
  hg_sum = np.zeros(7)
  hg_days = np.zeros(7)
  curr_day = 0
  for i in range(len(hg)):
    slice = hg.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      hg_days[int(curr_day) % 7] += 1
    if slice["Date"] != "---":
      hg_sum[int(slice["Date"]) % 7] += slice["# Trans"]
  for day in range(7):
    if hg_days[day] > 1:
      hg_sum[day] /= hg_days[day]

  mg = pd.read_csv("fulldata/Mary_Gates_Transactional_Data.csv")
  mg = mg[mg["Day Part"] == "---"]
  mg_sum = np.zeros(7)
  mg_days = np.zeros(7)
  curr_day = 0
  for i in range(len(mg)):
    slice = mg.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      mg_days[int(curr_day) % 7] += 1
    if slice["Date"] != "---":
      mg_sum[int(slice["Date"]) % 7] += slice["# Trans"]
  for day in range(7):
    if mg_days[day] > 1:
      mg_sum[day] /= mg_days[day]

  ms = pd.read_csv("fulldata/Microsoft_Transactional_Data.csv")
  ms = ms[ms["Day Part"] == "---"]
  ms_sum = np.zeros(7)
  ms_days = np.zeros(7)
  curr_day = 0
  for i in range(len(ms)):
    slice = ms.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      ms_days[int(curr_day) % 7] += 1
    if slice["Date"] != "---":
      ms_sum[int(slice["Date"]) % 7] += slice["# Trans"]
  for day in range(7):
    if ms_days[day] > 1:
      ms_sum[day] /= ms_days[day]

  op = pd.read_csv("fulldata/Orins_Sales.csv")
  op = op[op["Day Part"] == "---"]
  op_sum = np.zeros(7)
  op_days = np.zeros(7)
  curr_day = 0
  for i in range(len(op)):
    slice = op.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      op_days[int(curr_day) % 7] += 1
    if slice["Date"] != "---":
      op_sum[int(slice["Date"]) % 7] += slice["# Trans"]
  for day in range(7):
    if op_days[day] > 1:
      op_sum[day] /= op_days[day]

  ov = pd.read_csv("fulldata/Overpass Transactional Data.csv")
  ov = ov[ov["Day Part"] == "---"]
  ov_sum = np.zeros(7)
  ov_days = np.zeros(7)
  curr_day = 0
  for i in range(len(ov)):
    slice = ov.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      ov_days[int(curr_day) % 7] += 1
    if slice["Date"] != "---":
      ov_sum[int(slice["Date"]) % 7] += slice["# Trans"]
  for day in range(7):
    if ov_days[day] > 1:
      ov_sum[day] /= ov_days[day]

  ps = pd.read_csv("fulldata/Parnassus_Transactional_Data.csv")
  ps = ps[ps["Day Part"] == "---"]
  ps_sum = np.zeros(7)
  ps_days = np.zeros(7)
  curr_day = 0
  for i in range(len(ps)):
    slice = ps.iloc[i]
    if slice["Date"] != "---" and slice["Date"] != curr_day:
      curr_day = slice["Date"]
      ps_days[int(curr_day) % 7] += 1
    if slice["Date"] != "---":
      ps_sum[int(slice["Date"]) % 7] += slice["# Trans"]
  for day in range(7):
    if ps_days[day] > 1:
      ps_sum[day] /= ps_days[day]

  data = {
    "Weekday": weekdays.values(),
    "BG": bg_sum,
    "EG": eg_sum,
    "HG": hg_sum,
    "MG": mg_sum,
    "MS": ms_sum,
    "OP": op_sum,
    "OV": ov_sum,
    "PS": ps_sum
    }
  return pd.DataFrame(data)

"""
Returns dictionary where keys are each day of the week and values are DataFrames such that:
  Rows represent 30-minute timeslots
  Columns represent different locations
  Elements are true if locations are open, false otherwise
"""
def parsedHours():
  hours = pd.read_csv("data/Location_Hours.csv")
  times30 = times[::2]
  res = {}
  for day in range(7):
    df = pd.DataFrame({"Timeslot": times30})
    for i in range(len(hours)):
      location = hours["Location"].iloc[i]
      start = hours[str(weekdays[day])+"Open"].iloc[i]
      if start != "-":
        end = hours[str(weekdays[day])+"Close"].iloc[i]
        start_index = times30.index(start)
        end_index = times30.index(end)
        df[location] = [False] * start_index + [True] * (end_index - start_index)\
          + [False] * (len(times30) - end_index)
      else:
        df[location] = [False] * len(times30)
    res[weekdays[day]] = df
  return res

"""
Returns dictionary where keys are each day of the week and values are DataFrames such that:
  Rows represent 30-minute timeslots
  Columns represent different locations
  Elements are true if locations need workers, false otherwise
"""
def parsedStaffing():
  hours = pd.read_csv("data/Location_Staffing_Hours.csv")
  staff_times30 = staff_times[::2]
  res = {}
  for day in range(7):
    df = pd.DataFrame({"Timeslot": staff_times30})
    for i in range(len(hours)):
      location = hours["Location"].iloc[i]
      start = hours[str(weekdays[day])+"Open"].iloc[i]
      if start != "-":
        end = hours[str(weekdays[day])+"Close"].iloc[i]
        start_index = staff_times30.index(start)
        end_index = staff_times30.index(end)
        df[location] = [False] * start_index + [True] * (end_index - start_index)\
          + [False] * (len(staff_times30) - end_index)
      else:
        df[location] = [False] * len(staff_times30)
    res[weekdays[day]] = df
  return res

"""
Returns transactional data, but in 30-minute intervals instead of 15-minute intervals
"""
def parsedHalfHourData():
  data = parsedData()
  res = {}
  for weekday in data.keys():
    df15 = data[weekday]
    df30 = pd.DataFrame()
    for i in range(len(times[::2]) - 1):
      slice1 = df15.iloc[2 * i]
      slice2 = df15.iloc[2 * i + 1]
      df30.loc[i, "Timeslot"] = slice1["Timeslot"]
      for loc in locations:
        df30.loc[i, loc] = slice1[loc] + slice2[loc]
    res[weekday] = df30
  return res

if __name__ == "__main__":
  #print(parsedData())
  print(parsedTotals())
  #print(parsedHours())
  #print(parsedStaffing())
  #print(parsedHalfHourData())