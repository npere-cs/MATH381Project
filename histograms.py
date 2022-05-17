import numpy as np
import pandas as pd
import parsing
import matplotlib.pyplot as plt

trans_data = parsing.parsedHalfHourData()
mon_trans_data = trans_data["Mon"]
locations = ["BG", "EG", "HG", "MG", "MS", "OP", "OV", "PS"]
for loc in locations:
  ax = mon_trans_data.plot.bar(x="Timeslot", y=loc)
  fig = ax.get_figure()
  fig.savefig("graphs/Monday at " + loc + ".png")
ax = trans_data["Sat"].plot.bar(x="Timeslot", y="HG")
fig = ax.get_figure()
fig.savefig("graphs/Saturday at HG.png")