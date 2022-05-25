import numpy as np
import pandas as pd
import parsing
import matplotlib.pyplot as plt

locations = ["BG", "EG", "HG", "MG", "MS", "OP", "OV", "PS"]
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
"""
trans_data = parsing.parsedHalfHourData()
for day in weekdays:
  for loc in locations:
    ax = trans_data[day[0:3]].plot.bar(x="Timeslot", y=loc)
    fig = ax.get_figure()
    fig.savefig("graphs/" + day + " at " + loc + ".png")
ax = trans_data["Sat"].plot.bar(x="Timeslot", y="HG")
fig = ax.get_figure()
fig.savefig("graphs/Saturday at HG.png")
ax = trans_data["Sun"].plot.bar(x="Timeslot", y="HG")
fig = ax.get_figure()
fig.savefig("graphs/Sunday at HG.png")
"""
daily_averages = parsing.parsedTotals()
daily_averages = daily_averages.loc[:, daily_averages.columns!="Weekday"].transpose()
for i in range(len(weekdays)):
  ax = daily_averages.plot.bar(y=i)
  ax.get_legend().remove()
  fig = ax.get_figure()
  fig.savefig("graphs/" + weekdays[i] + " Totals.png")