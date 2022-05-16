import numpy as np
# from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
import pulp as p
import parsing
from itertools import compress

model = p.LpProblem(name="Heuristic", sense=p.LpMinimize)

# x = []
# for i in range(0, 24):
#   if (i < 10):
#     x.append(LpVariable(name="x0"+str(i), lowBound=0, cat="Integer"))
#   else:
#     x.append(LpVariable(name="x"+str(i), lowBound=0, cat="Integer"))
# for i in range(0, 6):
#   model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 2, str(i)+":00")
# for i in range(6, 10):
#   model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 8, str(i)+":00")
# for i in range(10, 12):
#   model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 4, str(i)+":00")
# for i in range(12, 16):
#   model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 3, str(i)+":00")
# for i in range(16, 18):
#   model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 6, str(i)+":00")
# for i in range(18, 22):
#   model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 5, str(i)+":00")
# for i in range(22, 24):
#   model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 3, str(i)+":00")
# model += lpSum(sum(x))
# status = model.solve()
# print(model)
# print(f"status: {model.status}, {LpStatus[model.status]}")
# print(f"objective: {model.objective.value()}")
# for var in model.variables():
#   print(f"{var.name}: {var.value()}")
# print()
# for name, constraint in model.constraints.items():
#   print(f"{name}: {constraint.value()}")

# represents number of FIXED classified positions at location
num_classified = {
  "MS": 0,
  "MG": 0,
  "PS": 0,
  "EG": 0,
  "BG": 0,
  "OP": 0,
  "HG": 0,
  "OV": 0
}

# represents the number of workers available to us on each day of week at each location
num_workers = {
  "Mon": 44,
  "Tue": 43,
  "Wed": 42,
  "Thu": 42,
  "Fri": 41,
  "Sat": 3,
  "Sun": 4
}

# Represents the abbreviated location codes
LOCATIONS = ["ms", "mg", "ps", "eg", "bg", "op", "hg", "ov"]

# Represent the time intervals at which individual
BUCKETS = [
  "06:30", "07:00", "07:30", "08:00", "08:30",
  "09:00",  "09:30", "10:00", "10:30", "11:00",
  "11:30", "12:00", "12:30", "13:00",  "13:30",
  "14:00",  "14:30", "15:00", "15:30", "16:00",
  "16:30", "17:00", "17:30", "18:00", "18:30"
]

'''
Shift lengths:
2 hrs, 2:30 hrs, 3 hrs, 3:30 hrs, 4 hrs, 4:30 hrs, 5 hrs
Classified (FIXED):
8:30 hrs
'''
# Represents the possible shift lengths employees can take on
# SHIFTS = ["2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00"]
SHIFTS = ["3:30"]

# # Fills the decision variables for each time bucket for regular employees
# for start_time in range(len(BUCKETS)):
#   shift_times = []
#   # Fills the shift lengths at the given time bucket
#   for shift in range(len(SHIFTS)):
#     shift_times.append(p.LpVariable(\
#       name=\
#       "People starting at " + BUCKETS[start_time] + "with " + SHIFTS[shift] + " long shift", \
#       lowBound=0, cat="Integer"))
#   # Fills decision variables for classified workers (8.5 hr fixed shift)
#   shift_times.append(p.LpVariable(\
#     name = "Classified starting at " + BUCKETS[start_time] + "with 8:30 long shift",\
#     lowBound=0, cat="Integer"))
#   dec_var.append(shift_times)



'''
MAX the sum of all the buckets such that the ratio of workers to transaction is maximized

sum up all transactional data within each bucket of time across all mondays

dictionary
key: value
weekday: df of (rows: ALL time buckets, cols: locations)


days of the week - outer
location - middle
buckets - deepest

'''

dec_var = []

# dictionary containing the transactional data for each day of the week at each location
# for each 30 minute interval
transacs = parsing.parsedHalfHourData()
# days of the week
weekdays = list(transacs.keys())
# locations
locations = list(transacs[weekdays[0]].columns[1:9])
print(locations)

hours = parsing.parsedHours()
staff_hrs = parsing.parsedStaffing()

# DECISION VARIABLE CREATION

# loop thru the days
for day in weekdays:
  # get the hours in which staff is needed
  staffage = staff_hrs[day]
  # loop thru the locations
  for location in locations:
    work_hours = list(compress(BUCKETS, staff_hrs[day][location]))
    # each possible time bucket
    for bucket in work_hours:
      for shift_len in SHIFTS:
        dec_var.append(p.LpVariable(\
        name="People starting at " + bucket + "with " + shift_len + " long shift", \
        lowBound=0, cat="Integer"))

# OBJECTIVE FUNCTION CONCATINATION

'''
for day in weekdays:
  transac_data = transacs[day]
  for location in locations:


first hour: only one decision var
2nd hour: two
3rd hour: three
4th


'''

# constraints
'''
minimum number of workers at each bucket has to be at least 2
  with the exception of weekends where there has to be at least 1

sum of all workers present on a given day can not exceed the number of workers that can
work on that day


'''