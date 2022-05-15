import numpy as np
# from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
import pulp as p

# MS LP

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
num_classified = 1

# represents the number of workers available to us on each day of week
num_workers = [8, 7, 7, 8, 7]

dec_var = []
'''
Times in which we can have employees start a shift in
7:00 7:30 8:00 ... 16:30 17:00

Shift lengths:
2 hrs, 2:30 hrs, 3 hrs, 3:30 hrs, 4 hrs, 4:30 hrs, 5 hrs
Classified (FIXED):
8:30 hrs

'''
BUCKETS = ["07:00", "07:30", "08:00", "08:30",
  "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", 
  "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", 
  "15:00", "15:30", "16:00", "16:30", "17:00", "17:30"]
SHIFTS = ["2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00"]

# Fills the decision variables for each time bucket for regular employees
for start_time in range(len(BUCKETS)):
  shift_times = []
  for shift in range(len(SHIFTS)):
    shift_times.append(p.LpVariable(\
      name="People starting at " + BUCKETS[start_time] + "with " + SHIFTS[shift] + " long shift", \
      lowBound=0, cat="Integer"))


# Fills decision variables for classified workers (8.5 hr fixed shift)
