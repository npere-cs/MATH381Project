import numpy as np
# from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
import pulp as p
import parsing

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
  "MS": [1, 2, 3, 4, 5, 6, 7],
  "MG": [1, 2, 3, 4, 5, 6, 7],
  "PS": [1, 2, 3, 4, 5, 6, 7],
  "EG": [1, 2, 3, 4, 5, 6, 7],
  "BG": [1, 2, 3, 4, 5, 6, 7],
  "HG": [1, 2, 3, 4, 5, 6, 7],
  "OV": [1, 2, 3, 4, 5, 6, 7]
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
SHIFTS = ["2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00"]

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

# # loop thru the days
# for day in weekdays:
#   locations = []
  
#   headers = df.columns
#   # loop thru the locations
#   for 
