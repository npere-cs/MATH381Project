import numpy as np
# from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
import pulp as p
import parsing
import math
from itertools import compress

# represents number of FIXED classified positions at location
num_classified = {
  "BG": 0,
  "EG": 1, # originally 2
  "HG": 0,
  "MG": 0,
  "MS": 1, # originally 1
  "OP": 0,
  "OV": 1, # originally 1
  "PS": 1
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
LOCATIONS = ["BG", "EG", "HG", "MG", "MS", "OP", "OV", "PS"]

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

# dictionary containing the transactional data for each day of the week at each location
# for each 30 minute interval
transacs = parsing.parsedHalfHourData()
# days of the week
weekdays = list(transacs.keys())
# locations
locations = list(transacs[weekdays[0]].columns[1:9])

hours = parsing.parsedHours()
# print(hours)
staff_hrs = parsing.parsedStaffing()

'''
Apportionment problem:
for each day of the week:
 - take the total of all average transactions
 - divide by total number of workers provided for that day (? include CLASSIFIED)
 - this will give us STD DIVISOR

 - divide each location's average transactions and divide by STD DIVISOR to get QUOTA
 - lower quota: n = Math.floor(QUOTA)
 - geometric mean: sqrt(n * (n + 1))
 - get the initial allocation thru sum of all:
 - if quota > geom mean, Math.ceil(QUOTA)
 - if quota < geom mean, Math.floor(QUOTA)

 - if initial allocation < number of workers decrease the divisor
 - if initial allocation > number of workers increase the divisor
'''

'''
Function that accepts average transactional data for different locations at a particular day,
as well as the total number of workers available to apportion during that day. Returns a list
of the number of workers to allocate to each location
'''
def apportionment(data, workers):
  INCREMENT = 0.1
  allocation = [0] * len(data)
  divisor = sum(data) / workers
  quotas = [0] * len(data)
  iterations = 0
  while (sum(allocation) != workers):
    iterations += 1
    for idx in range(len(data)):
      quotas[idx] = data[idx] / divisor
      lower_quota = math.floor(quotas[idx])
      geom_mean = math.sqrt(lower_quota * (lower_quota + 1))
      if quotas[idx] > geom_mean:
        allocation[idx] = math.ceil(quotas[idx])
      else:
        allocation[idx] = math.floor(quotas[idx])
    if iterations % 100 == 0:
      INCREMENT /= 10
    if iterations == 500: # DEBUGGING CODE
      # print("OVERFLOW: EXCEEDS REASONABLE NUM ITERATIONS")
      # print("Current allocation: " + str(allocation) + "\nwith sum: " + str(sum(allocation)) \
      #   + ", desired sum = " + str(workers))
      break
    if (sum(allocation) < workers):
      divisor -= INCREMENT
    else: # (sum(allocation) > workers)
      divisor += INCREMENT
  # print("num iters: " + str(iterations))
  return allocation

# Parsed Transactional Data
data = parsing.parsedTotals()
workdays = weekdays[0:5]

# Dictionary that stores the key: value pair as DAY: ALLOCATIONS
allocated_workers_day = {}

# Determines the allocation of individual workers to each location on each day
for day in range(len(workdays)):
  day_data = list(data.iloc[day])[1:9]
  workers = num_workers[workdays[day]]
  allocation = apportionment(day_data, workers)
  allocated_workers_day[workdays[day]] = allocation
  # print(workdays[day])
  # print(allocation)
  # print("Allocated: " + str(sum(allocation)) + ", with actual: " + str(num_workers[workdays[day]]))

apportionment_data = [None] * len(workdays) # [day of week][location idx][allocations (different lens)]

# Performs apportionment for each day and for each location using transactional data
# Apportions MAX number of half-hours that can be worked at the location
for day in range(len(workdays)):
  day_transacs = transacs[workdays[day]]
  operating_hours = hours[workdays[day]]
  apportionment_at_location = [None] * len(LOCATIONS) # setting up array of locations
  for location in range(len(LOCATIONS)):
    location_hours = list(operating_hours[LOCATIONS[location]])
    # indicies of locations' open and close times
    idx_open = location_hours.index(True)
    idx_close = len(location_hours) - location_hours[::-1].index(True) - 1
    location_transacs = list(day_transacs[LOCATIONS[location]])

    location_transacs = location_transacs[idx_open:idx_close + 1]
    # print("Location: " + locations[location] + str(location_transacs))
    workers = allocated_workers_day[workdays[day]][location]
    allocated_hours = apportionment(location_transacs, (10 * workers + 17 * num_classified[LOCATIONS[location]]))
    apportionment_at_location[location] = allocated_hours # saves allocation data to the location
    # print("Location: " + LOCATIONS[location] + " on " + workdays[day] + "\n" + str(allocated_hours))
  apportionment_data[day] = apportionment_at_location # saving the day to the apportionment 3D array

# for day in range(len(apportionment_data)):
#   print(str(workdays[day]) + ": ")
#   for location in apportionment_data[day]:
#     print(location)

'''
Determines the work schedules at a particular location provided apportionment data, the number of workers
and the staffing schedule

Universal constraints:
*  At least 2 people working at any given time
'''
def scheduler(apportionment, num_workers, staff_hrs, classified_amt, lp_name):
  model = p.LpProblem(name=lp_name, sense=p.LpMaximize)

  # Decision variable creation
  classified_vars = []
  work_hours = list(compress(BUCKETS, staff_hrs))
  num_buckets = len(work_hours)
  active_workers = [[] for i in range(num_buckets)] # 2D Array for active workers at a time active_workers[current_time][shift_of_workers]
  shift_scores = [] # 2D Array to favor shifts closer to 3.5 hours
  scores = [3, 3, 4, 5, 3, 3, 2]
  dec_var = [] # 2D Array for Decision Vars dec_var[time_shift_start][shift_length]

  for bucket_idx in range(num_buckets): # Goes through the indicies of the possible times that staff can start a shift
    # Regular job decision variables
    shifts_at_bucket = [] # stores the possible shifts that can be started at the current time bucket
    scores_at_bucket = []
    for shift_idx in range(len(SHIFTS)): # goes through the indicies of the possible shift lengths
      if ((4 + shift_idx + bucket_idx) <= num_buckets): # checks to make sure that the shift is feasible provided the number of time left in the work day
        var = p.LpVariable(\
          name="Start: " + work_hours[bucket_idx] + " Shift: " + SHIFTS[shift_idx], lowBound=0, cat="Integer")
        for work_bucket in range(4 + shift_idx): # this loop fills in when workers are actively working
          active_workers[bucket_idx + work_bucket].append(var)
        shifts_at_bucket.append(var) # work_hours[bucket_idx] + " " + SHIFTS[shift_idx]
        scores_at_bucket.append(scores[shift_idx])
        # shifts_at_bucket.append(p.LpVariable(\
        #   name="People starting at " + work_hours[bucket_idx] + " with " + SHIFTS[shift_idx] + " long shift", \
        #   lowBound=0, cat="Integer"))

    # Classified job decision variable
    for classified in range(classified_amt):
      if ((17 + bucket_idx) <= num_buckets): # checks whether the classified position starting at the current time is feasible
        var = p.LpVariable(\
          name="Start: " + work_hours[bucket_idx], lowBound=0, cat="Integer")
        for work_bucket in range(17): # adds the classified position as an active worker at each appropriate position
          active_workers[bucket_idx + work_bucket].append(var) # work_hours[bucket_idx] + " " + "8:30 CF"\
        classified_vars.append(var) # work_hours[bucket_idx] + " " + "8:30 CF"

    dec_var.append(shifts_at_bucket)
    shift_scores.append(scores_at_bucket)
  # FOR DEBUGGING
  # for i in range(len(dec_var)):
  #   print(dec_var[i])
  # print(classified_vars)

  # Objective function
    # max sum of all decision variables
  obj = p.lpSum(classified_vars)
  for bucket in dec_var:
    obj += p.lpSum(bucket)

  # constraint definitions
  # at least 2 people working at any given time
    # when num_workers + classified workers > 5, make at least 2 people present, otherwise make at least 1 person present
  min_workers = 1
  if num_workers + classified_amt > 5:
    # make at least 2 people present at each time
    min_workers = 2

  for bucket_idx in range(len(active_workers)):
    constraint = (p.lpSum(active_workers[bucket_idx]) >= min_workers, "Min workers at " + str(work_hours[bucket_idx]))
    model += constraint

  # sum of all classified shifts must equal num classified at location
  model += (p.lpSum(classified_vars) == classified_amt, "Req. amount Classified")

  # DUMMY constraint: sum of all decision variables <= allocated workers
  model += (obj == num_workers + classified_amt, "Worker limit")

  # the max number of workers at each time bucket is the number in the apportionment data + 2
  min_apportionment = [(apportionment[i] / 2) for i in range(len(apportionment))]
  # print("length of active workers arr: " + str(len(active_workers)))
  # print("length of apportionment data: " + str(len(max_apportionment)))
  for bucket_idx in range(len(active_workers)):
    if bucket_idx != 0 and bucket_idx != (len(active_workers) - 1):
      model += (p.lpSum(active_workers[bucket_idx]) >= min_apportionment[bucket_idx - 1], "Rec. min workers at " + str(work_hours[bucket_idx]))

  obj = p.lpSum(classified_vars)
  for i in range(len(dec_var)):
    obj += p.lpSum(np.dot(dec_var[i], shift_scores[i]))
  model += obj

  # solves the model
  status = model.solve()
  print(status)
  # prints out the resulting decision variables
  # for var in model.variables():
  #   print(str(var) + ": " + str(p.value(var)))
  # for name, constraint in model.constraints.items():
  #   print(f"{name}: {constraint.value()}")
  return model

'''
BG, EG, HG, MG should each have 1 classified worker

'''
# print(staff_hrs["Mon"])
# print(allocated_workers_day["Mon"][4])
# scheduler(apportionment_data[0][4], allocated_workers_day["Mon"][4], staff_hrs["Mon"]["MS"], num_classified["MS"], "MS_Mon")

# loop containing the way to solve all LPs
for day_idx in range(len(workdays)):
  weekday = workdays[day_idx]
  print(weekday)
  for location_idx in range(len(LOCATIONS)):
    location = LOCATIONS[location_idx]
    print(location)
    model = scheduler(apportionment_data[day_idx][location_idx], allocated_workers_day[weekday][location_idx], \
      staff_hrs[weekday][location], num_classified[location], location + "_" + weekday)
    f = open(location + "_" + weekday + ".txt", "w")
    for var in model.variables():
      f.write(str(var) + ": " + str(p.value(var)) + "\n")
    f.close()