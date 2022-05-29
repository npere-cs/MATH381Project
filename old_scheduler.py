import math
import numpy as np
import pulp as p
import pandas as pd
import matplotlib.pyplot as plt
from itertools import compress

SHIFTS = ["2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00"]
BUCKETS = [
  "06:30", "07:00", "07:30", "08:00", "08:30",
  "09:00",  "09:30", "10:00", "10:30", "11:00",
  "11:30", "12:00", "12:30", "13:00",  "13:30",
  "14:00",  "14:30", "15:00", "15:30", "16:00",
  "16:30", "17:00", "17:30", "18:00", "18:30"
]
all_data = [
  [["C1", 0, 17], ["E1", 1, 6], ["E2", 7, 6], ["E3", 12, 5], ["E4", 16, 3]], # OV Wed
  [["E1", 2, 8], ["E2", 3, 8], ["E3", 9, 6], ["E4", 15, 9]], # HG Fri
  [["E1", 1, 6], ["E2", 3, 4], ["E3", 6, 6], ["E4", 7, 6], ["E5", 8, 6], ["E6", 8, 6], ["E7", 10, 6], ["E8", 14, 4], ["E9", 15, 5], ["E10", 16, 4]], # BG Thurs
  [["E1", 1, 6], ["E2", 3, 9], ["E3", 5, 8], ["C1", 5, 17], ["E4", 8, 8], ["E5", 13, 7], ["E6", 16, 5]] # MS Tue
]
examples = [["OV", "Wed"], ["HG", "Fri"], ["BG", "Thu"], ["MS", "Tue"]]
for i in range(len(examples)):
  data = all_data[i]
  loc = examples[i][0]
  day = examples[i][1]
  df = pd.DataFrame(data, columns=["Name", "Start", "Len"])
  x_bins = np.arange(len(BUCKETS))
  fig, gnt = plt.subplots()
  gnt.barh(df.Name, df.Len, left=df.Start)
  gnt.set_xticks(np.arange(len(BUCKETS)))
  gnt.set_xticklabels(BUCKETS, rotation=90)
  plt.subplots_adjust(bottom=0.2)
  plt.xlabel("Time")
  plt.ylabel("Employee")
  plt.grid(axis="x")
  plt.gca().invert_yaxis()
  plt.title("Original Employee Schedules for " + loc + " on " + day)
  plt.savefig("schedules/old_schedules/" + loc + "_" + day + ".png")