import numpy as np
import pandas as pd

weekdays = {0: "Mon", 1:"Tue", 2:"Wed", 3:"Thu", 4: "Fri", 5: "Sat", 6:"Sun"} # remember to % 7

"""
Relevant Info to Parse:
  Day of the week
  Time period
  # transactions (seems to be equivalent to guests/tables)
  Net sales? (this or the one below is a metric for how busy people are preparing stuff)
  Average sales per transaction?
"""
def parsedData(filename):
  all_data = pd.read_csv(filename)
  return None