import numpy as np
import pandas as pd
import parsing
import matplotlib.pyplot as plt

locations = ["BG", "EG", "HG", "MG", "MS", "OP", "OV", "PS"]
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
daily_apportionments = pd.DataFrame([
  [5, 4, 4, 3, 6, 11, 5, 6],
  [4, 4, 4, 3, 6, 11, 5, 6],
  [4, 4, 4, 3, 7, 10, 4, 6],
  [4, 4, 4, 3, 6, 10, 5, 6],
  [4, 5, 5, 3, 7, 6, 5, 6]
], columns=locations).transpose()
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
print(daily_averages)
print(daily_apportionments)
for i in range(len(weekdays)):
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax2 = ax.twinx()
  daily_averages.plot(kind="bar", y=i, color="blue", ax=ax, width=0.25, position=1, legend=None, title="Transactions and Workers on " + weekdays[i])
  daily_apportionments.plot(kind="bar", y=i, color="black", ax=ax2, width=0.25, position=0, legend=None)
  ax.set_ylabel("Average Transactions")
  ax2.set_ylabel("Workers Assigned", rotation=270)
  ax.set_xticklabels(locations, rotation=0)
  fig = ax.get_figure()
  fig.savefig("graphs/" + weekdays[i] + " Totals.png")