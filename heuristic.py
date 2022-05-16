import numpy as np
# from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
import pulp as p
import parsing
from itertools import compress

# model = p.LpProblem(name="Heuristic", sense=p.LpMinimize)

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
SHIFTS = ["2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00"]
# SHIFTS = ["3:30"]

# dictionary containing the transactional data for each day of the week at each location
# for each 30 minute interval
transacs = parsing.parsedHalfHourData()
# days of the week
weekdays = list(transacs.keys())
# locations
locations = list(transacs[weekdays[0]].columns[1:9])

hours = parsing.parsedHours()
staff_hrs = parsing.parsedStaffing()

# DECISION VARIABLE CREATION


staffage = staff_hrs["Mon"]
work_hours = list(compress(BUCKETS, staffage["MS"]))
# print(work_hours)
num_buckets = len(work_hours)
active_workers = [] # 2D Array for active workers at a time active_workers[current_time][shift_of_workers]

# creates an empty structure where we can store the people working at each time bucket
for bucket_idx in range(num_buckets):
  active_workers.append([])

classified = []
dec_var = [] # 2D Array for Decision Vars dec_var[time_shift_start][shift_length]
for bucket_idx in range(num_buckets): # Goes through the indicies of the possible times that staff can start a shift
  shifts_at_bucket = [] # stores the possible shifts that can be started at the current time bucket
  for shift_idx in range(len(SHIFTS)): # goes through the indicies of the possible shift lengths
    if ((4 + shift_idx + bucket_idx) <= num_buckets): # checks to make sure that the shift is feasible provided the number of time left in the work day
      var = p.LpVariable(\
        name="People starting at " + work_hours[bucket_idx] + " with " + SHIFTS[shift_idx] + " long shift", \
        lowBound=0, cat="Integer")
      for work_bucket in range(4 + shift_idx): # this loop fills in when workers are actively working
        active_workers[bucket_idx + work_bucket].append(var) # work_hours[bucket_idx] + " " + SHIFTS[shift_idx]
      shifts_at_bucket.append(var) # work_hours[bucket_idx] + " " + SHIFTS[shift_idx]
      # shifts_at_bucket.append(p.LpVariable(\
      #   name="People starting at " + work_hours[bucket_idx] + " with " + SHIFTS[shift_idx] + " long shift", \
      #   lowBound=0, cat="Integer"))
  if ((17 + bucket_idx) <= num_buckets): # checks whether the classified position starting at the current time is feasible
    var = p.LpVariable(\
      name="Classified starting at " + work_hours[bucket_idx] + " with 8:30 long shift", \
       lowBound=0, cat="Integer")
    for work_bucket in range(17): # adds the classified position as an active worker at each appropriate position
      active_workers[bucket_idx + work_bucket].append(var) # work_hours[bucket_idx] + " " + "8:30 CF"
    classified.append(var) # work_hours[bucket_idx] + " " + "8:30 CF"
  dec_var.append(shifts_at_bucket)


# print(dec_var)
# print(active_workers)

workers_MS_Mon = 6
classified_MS_Mon = 1




MS_mon_model = p.LpProblem(name="Heuristic", sense=p.LpMaximize)

# OBJECTIVE FUNCTION

transac_data_mon = transacs["Mon"]
MS_mon_transac = list(transac_data_mon["MS"])[0:(21 + 1)]
obj = 0
for transac_index in range(len(MS_mon_transac)):
  if not (MS_mon_transac[transac_index] <= 0.00001):
    obj += p.lpSum(active_workers[transac_index]) / MS_mon_transac[transac_index]

MS_mon_model += obj

# constraints
'''
minimum number of workers at each bucket has to be at least 2
  with the exception of weekends where there has to be at least 1

sum of all workers present on a given day can not exceed the number of workers that can
work on that day
'''
# min of 2 workers at any given time
for workers in active_workers:
  MS_mon_model += p.lpSum(workers) >= 2

# sum of all classified shifts equals to the number of classified workers required
MS_mon_model += p.lpSum([classified[i] for i in range(len(classified))]) == classified_MS_Mon

# sum of all shifts must equal to the number of workers allocated to MS on Mon
MS_mon_model += p.lpSum([dec_var[i][j] for i in range(len(dec_var)) for j in range(len(dec_var[i]))]) == workers_MS_Mon

status = MS_mon_model.solve()