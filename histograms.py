import numpy as np
import pandas as pd
import parsing
import matplotlib.pyplot as plt

locations = ["BG", "EG", "HG", "MG", "MS", "OP", "OV", "PS"]
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
buckets = [
  "07:00", "07:30", "08:00", "08:30",
  "09:00",  "09:30", "10:00", "10:30", "11:00",
  "11:30", "12:00", "12:30", "13:00",  "13:30",
  "14:00",  "14:30", "15:00", "15:30", "16:00",
  "16:30", "17:00", "17:30"
]
daily_apportionments = pd.DataFrame([
  [5, 4, 4, 3, 6, 11, 5, 6],
  [4, 4, 4, 3, 6, 11, 5, 6],
  [4, 4, 4, 3, 7, 10, 4, 6],
  [4, 4, 4, 3, 6, 10, 5, 6],
  [4, 5, 5, 3, 7, 6, 5, 6]
], columns=locations).transpose()
min_workers = {
  "Mon": pd.DataFrame([
    [0, 0, 0.4, 0.4, 0.8, 0.8, 1.2, 1.2, 1.6, 1.6, 2.0, 1.6, 1.6, 1.2, 1.6, 1.6, 1.6, 0.8, 0, 0, 0, 0],
    [0, 0.4, 0.4, 0.8, 1.6, 1.2, 1.2, 1.6, 1.6, 2.0, 2.0, 2.0, 1.6, 1.6, 1.2, 1.2, 1.2, 0.4, 0.4, 0.4, 0, 0],
    [0.4, 0.4, 0.8, 0.8, 0.8, 1.2, 1.2, 0.8, 0.8, 1.2, 0.8, 1.2, 0.8, 0.8, 0.4, 0.8, 0.4, 0.8, 0.4, 0.4, 0.4, 0.4],
    [0, 0.4, 0.4, 0.4, 0.8, 0.8, 1.2, 0.8, 1.2, 0.8, 1.2, 1.2, 0.8, 0.8, 0.8, 0.4, 0, 0, 0, 0, 0, 0],
    [0, 0.4, 1.2, 0.8, 1.6, 1.6, 1.6, 2.0, 2.0, 1.6, 2.8, 2.4, 2.4, 2.0, 2.0, 1.6, 1.6, 1.2, 1.2, 0.8, 0, 0],
    [0.4, 0.8, 1.6, 0.8, 1.6, 2.8, 3.2, 1.6, 2.4, 3.2, 4.4, 3.6, 4.4, 2.0, 2.4, 2.8, 3.6, 1.2, 1.6, 1.6, 2.4, 2.4],
    [0, 0.8, 1.2, 1.6, 2.0, 2.0, 2.0, 2.0, 2.0, 1.6, 2.0, 2.4, 2.0, 1.6, 1.2, 1.2, 0.8, 0.4, 0, 0, 0, 0],
    [0, 0.4, 0.4, 0.4, 0.8, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 2.0, 2.0, 1.6, 1.6, 1.6, 0.8, 1.2, 0.8, 0.4, 0.4, 0]
  ]).transpose(),
  "Tue": pd.DataFrame([
    [0, 0, 0.4, 0.4, 0.8, 0.8, 0.8, 0.8, 1.2, 0.8, 1.2, 1.6, 1.2, 1.2, 1.6, 1.2, 1.2, 0.8, 0, 0, 0, 0],
    [0, 0.4, 0.8, 0.8, 1.2, 1.2, 1.6, 1.2, 2.0, 2.0, 2.0, 2.0, 1.6, 1.2, 1.2, 1.2, 1.2, 0.4, 0.4, 0.4, 0, 0],
    [0.8, 0.4, 0.8, 0.8, 0.8, 1.2, 1.2, 0.8, 1.2, 0.8, 1.2, 0.8, 0.8, 0.8, 0.8, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
    [0, 0.4, 0.8, 0.4, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1.6, 0.8, 0.8, 0.8, 0.8, 0.8, 0, 0, 0, 0, 0, 0],
    [0, 0.4, 0.8, 0.8, 1.6, 1.6, 2.0, 1.2, 1.6, 2.4, 2.4, 2.8, 2.4, 1.6, 2.0, 1.6, 1.6, 1.6, 1.6, 0.8, 0, 0],
    [0.4, 0.4, 1.2, 0.8, 1.6, 2.0, 3.2, 2.0, 2.0, 3.2, 4.4, 3.6, 4.8, 2.0, 2.8, 3.2, 4.0, 2.4, 2.0, 1.2, 1.6, 2.0],
    [0, 1.2, 1.6, 1.6, 1.6, 2.0, 2.0, 1.6, 2.0, 2.0, 2.4, 2.4, 1.6, 1.2, 1.2, 1.2, 0.8, 0.4, 0, 0, 0, 0],
    [0, 0.4, 0.8, 0.8, 0.8, 1.2, 1.2, 1.6, 1.6, 1.6, 1.2, 1.6, 1.6, 2.0, 1.6, 1.2, 1.2, 1.2, 1.2, 0.8, 0.4, 0]
  ]).transpose(),
  "Wed": pd.DataFrame([
    [0, 0, 0.4, 0.4, 0.8, 0.4, 1.2, 1.2, 1.2, 1.2, 1.6, 1.2, 1.2, 1.2, 1.2, 1.2, 0.8, 0.8, 0, 0, 0, 0],
    [0, 0.4, 0.8, 0.8, 1.2, 0.8, 1.2, 2.0, 1.6, 1.6, 1.6, 2.0, 1.2, 1.6, 1.6, 2.0, 1.2, 0.4, 0.4, 0.4, 0, 0],
    [0.4, 0.4, 0.8, 0.8, 1.2, 0.8, 1.6, 1.2, 0.8, 1.2, 0.8, 1.2, 0.8, 0.8, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
    [0, 0.4, 0.4, 0.4, 0.8, 0.4, 1.6, 0.8, 1.2, 0.8, 1.2, 0.8, 0.8, 0.8, 0.8, 0.8, 0, 0, 0, 0, 0, 0],
    [0, 0.8, 1.2, 1.2, 1.6, 2.0, 2.0, 2.4, 2.0, 2.4, 2.8, 2.8, 2.4, 2.0, 1.6, 1.6, 2.0, 1.6, 1.2, 1.2, 0, 0],
    [0.4, 0.8, 1.6, 0.8, 1.2, 2.0, 2.8, 1.6, 2.4, 2.0, 4.4, 3.6, 3.2, 2.4, 2.0, 2.8, 3.2, 1.6, 1.6, 1.6, 2.0, 2.8],
    [0, 0.8, 1.2, 1.2, 1.6, 1.6, 1.6, 1.6, 1.6, 2.0, 2.0, 2.0, 1.6, 0.8, 1.2, 0.8, 0.8, 0.4, 0, 0, 0, 0],
    [0, 0.4, 0.8, 0.8, 1.2, 1.2, 1.6, 1.6, 1.6, 1.6, 1.6, 2.0, 1.6, 1.6, 1.6, 1.2, 0.8, 1.2, 0.8, 0.4, 0.4, 0]
  ]).transpose(),
  "Thu": pd.DataFrame([
    [0, 0, 0.4, 0.4, 0.4, 0.8, 0.8, 1.2, 1.2, 0.8, 1.6, 1.6, 1.2, 1.2, 1.2, 1.2, 1.2, 0.8, 0, 0, 0, 0],
    [0, 0.4, 0.4, 1.2, 1.2, 1.2, 1.6, 1.2, 1.6, 2.4, 2.4, 2.0, 1.6, 1.2, 1.2, 1.2, 0.8, 0.4, 0.4, 0.4, 0, 0],
    [0.4, 0.4, 0.8, 1.2, 1.2, 1.2, 1.2, 0.8, 0.8, 1.2, 0.8, 1.2, 0.8, 0.4, 0.8, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
    [0, 0.4, 0.8, 0.4, 0.8, 0.8, 1.2, 0.8, 0.8, 0.8, 1.2, 0.8, 0.8, 0.8, 0.8, 0.8, 0, 0, 0, 0, 0, 0],
    [0, 0.4, 1.2, 1.2, 1.6, 1.6, 2.4, 1.6, 1.6, 2.0, 2.4, 2.4, 2.4, 2.0, 2.0, 1.6, 1.6, 1.2, 0.8, 0.8, 0, 0],
    [0.4, 0.4, 0.8, 1.2, 1.6, 1.6, 2.8, 2.0, 2.4, 2.4, 4.0, 3.6, 3.6, 2.4, 2.4, 2.8, 4.0, 1.6, 1.6, 1.6, 2.0, 1.6],
    [0, 0.8, 1.6, 1.6, 2.0, 1.6, 2.0, 1.6, 2.0, 1.6, 2.8, 2.0, 2.0, 1.2, 1.6, 0.8, 1.2, 0.4, 0, 0, 0, 0],
    [0, 0.4, 0.8, 0.4, 1.2, 1.2, 1.6, 1.6, 1.6, 1.6, 1.6, 2.0, 1.6, 1.6, 1.6, 1.2, 1.2, 0.8, 0.8, 0.8, 0.4, 0]
  ]).transpose(),
  "Fri": pd.DataFrame([
    [0, 0, 0.4, 0.4, 0.8, 0.4, 1.2, 1.6, 1.6, 1.2, 1.6, 0.8, 1.2, 1.2, 1.6, 0.8, 0.4, 0.8, 0, 0, 0, 0],
    [0, 0.4, 0.8, 0.8, 2.0, 1.2, 2.0, 1.6, 2.8, 2.0, 2.0, 2.0, 2.0, 2.4, 1.6, 1.2, 0.8, 0.4, 0.4, 0.4, 0, 0],
    [0.8, 0.8, 0.8, 0.8, 1.2, 1.2, 2.0, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 0.8, 0.8, 0.8, 0.4, 0.8, 0.4, 0.4, 0.4, 0.4],
    [0, 0.4, 0.4, 0.8, 0.8, 0.8, 1.2, 1.2, 1.2, 0.8, 1.2, 0.8, 0.8, 0.4, 0.8, 0.4, 0, 0, 0, 0, 0, 0],
    [0, 0.4, 1.2, 1.6, 2.4, 2.0, 2.0, 1.6, 2.4, 2.4, 3.2, 2.4, 2.4, 2.4, 2.0, 1.6, 1.6, 1.2, 1.2, 0.8, 0, 0],
    [0.4, 0.4, 0.8, 0.8, 1.6, 2.0, 2.0, 2.4, 2.0, 2.0, 2.8, 2.8, 3.2, 3.2, 2.4, 2.0, 0, 0, 0, 0, 0, 0],
    [0, 0.8, 1.6, 1.6, 2.0, 1.6, 1.6, 2.0, 2.0, 1.6, 2.8, 2.0, 2.0, 1.6, 1.6, 0.8, 0.8, 0.4, 0, 0, 0, 0],
    [0, 0.4, 0.8, 0.8, 1.2, 1.2, 1.6, 2.8, 2.0, 1.6, 2.0, 1.6, 1.2, 1.6, 1.2, 1.2, 0.8, 0.8, 0.4, 0.4, 0.4, 0]
  ]).transpose()
}

trans_data = parsing.parsedHalfHourData()
for day in weekdays:
  curr_trans = trans_data[day[0:3]]
  curr_work = min_workers[day[0:3]]
  print(curr_trans)
  print(curr_work)
  for j in range(len(locations)):
    loc = locations[j]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    curr_trans.plot(kind="bar", y=loc, ax=ax, legend=None, title="Transactions and Minimum Workers on " + day + " at " + loc)
    ax.set_ylabel("Average Transactions")
    ax.set_xlabel("Time")
    ax.set_xticklabels(buckets)
    fig = ax.get_figure()
    fig.subplots_adjust(bottom=0.2, left=0.1)
    fig.savefig("graphs/" + day + " at " + loc + ".png")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    curr_trans.plot(kind="bar", y=loc, ax=ax, width=0.4, position=1, legend=None, title="Transactions and Minimum Workers on " + day + " at " + loc)
    curr_trans.plot(kind="bar", y=loc, ax=ax, width=0.4, position=1, legend=None, title="Transactions and Minimum Workers on " + day + " at " + loc)
    curr_work.plot(kind="bar", y=j, color="black", ax=ax2, width=0.4, position=0, legend=None)
    ax.set_ylabel("Average Transactions")
    ax2.set_ylabel("Minimum Workers", rotation=270, labelpad=15)
    ax.set_xlabel("Time")
    ax.set_xticklabels(buckets)
    fig = ax.get_figure()
    fig.subplots_adjust(bottom=0.2)
    fig.savefig("graphs/Compare " + day + " at " + loc + ".png")

daily_averages = parsing.parsedTotals()
daily_averages = daily_averages.loc[:, daily_averages.columns!="Weekday"].transpose()
for i in range(len(weekdays)):
  fig = plt.figure()
  ax = fig.add_subplot(111)
  daily_averages.plot(kind="bar", y=i, ax=ax, width=0.25, legend=None, title="Transactions and Workers on " + weekdays[i])
  ax.set_ylabel("Average Transactions")
  ax.set_xticklabels(locations, rotation=0)
  fig = ax.get_figure()
  fig.savefig("graphs/" + weekdays[i] + " Totals.png")

  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax2 = ax.twinx()
  daily_averages.plot(kind="bar", y=i, ax=ax, width=0.25, position=1, legend=None, title="Transactions and Workers on " + weekdays[i])
  daily_apportionments.plot(kind="bar", y=i, color="black", ax=ax2, width=0.25, position=0, legend=None)
  ax.set_ylabel("Average Transactions")
  ax2.set_ylabel("Workers Assigned", rotation=270)
  ax.set_xlabel("Location")
  ax.set_xticklabels(locations, rotation=0)
  fig = ax.get_figure()
  fig.savefig("graphs/Compare " + weekdays[i] + " Totals.png")
