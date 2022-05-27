import math
import numpy as np
import pulp as p
from itertools import compress
import parsing # contains the parsed data

# represents number of FIXED classified positions at location
NUM_CLASSIFIED = {
  "BG": 0,
  "EG": 1, # originally 2
  "HG": 0,
  "MG": 0,
  "MS": 1, # originally 1
  "OP": 1,
  "OV": 1, # originally 1
  "PS": 0 # originally 0 (CANNOT HAVE CLASSIFIED WORKERS)
}

# CAN BE MODIFIED TO REFLECT REALIZED LABOR RESOURCES ON EACH DAY OF THE WEEK
# represents the number of workers available to us on each day of week at each location
# Note: SAT AND SUN WORKERS WERE NOT CONSIDERED FOR THIS MODEL
NUM_WORKERS = {
  "Mon": 44, # originally 44
  "Tue": 43, # originally 43
  "Wed": 42, # originally 42
  "Thu": 42, # originally 42
  "Fri": 41, # originally 41
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

# Represents the possible shift lengths employees can take on
SHIFTS = ["2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00"]
# preference scores on a scale of 1 to 5 1 being least preferred and 5 being most preferred
SCORES = [3, 3, 4, 5, 3, 3, 2]

# dictionary containing the transactional data for each day of the week at each location
# for each 30 minute interval
transacs = parsing.parsedHalfHourData()

# days of the week
weekdays = list(transacs.keys())

# locations
locations = list(transacs[weekdays[0]].columns[1:9])

# contains dictionary of dataframes that have TRUE/FALSE for each possible time bucket of
# operation at each location
hours = parsing.parsedHours()

# contains dictionary of dataframes that have TRUE/FALSE for each possible time bucket of
# scheduled staff hours at each location
staff_hrs = parsing.parsedStaffing()

'''
Function that accepts average transactional data for different locations at a particular day,
as well as the total number of workers available to apportion during that day. Returns a list
of the number of workers to allocate to each location

Code is a slightly modified version of:
https://theuforce.blogspot.com/2010/12/python-huntington-hill-method.html

This function generates the same results as the first apportionment function, but this is more
clear as to what is going on (the formula can be nicely inferred from this function [see wiki])
https://en.wikipedia.org/wiki/Huntington%E2%80%93Hill_method
https://en.wikipedia.org/wiki/United_States_congressional_apportionment#The_method_of_equal_proportions
'''
def apportionment(data, workers):
  num_locations = len(data)
  allocation = [1] * num_locations # initial apportionment, at least 1 worker per location
  geom_means = [math.sqrt(2)] * num_locations
  for i in range(num_locations, workers):
    max = 0
    for location in range(1, num_locations):
      if (data[location] / geom_means[location]) > (data[max] / geom_means[max]):
        max = location
    allocation[max] +=  1
    geom_means[max] = math.sqrt(allocation[max] * (allocation[max] + 1))
  return allocation

# Parsed Transactional Data
data = parsing.parsedTotals()
workdays = weekdays[0:5]

# Dictionary that stores the key: value pair as DAY: ALLOCATIONS
allocated_workers_day = {}

# Determines the allocation of individual workers to each location on each day
for day in range(len(workdays)):
  day_data = list(data.iloc[day])[1:9]
  workers = NUM_WORKERS[workdays[day]]
  allocation = apportionment(day_data, workers)
  allocated_workers_day[workdays[day]] = allocation
  # DEBUGGING CODE - prints out the allocations
  # print(workdays[day])
  # print(allocation)
  # print("Allocated: " + str(sum(allocation)) + ", with actual: " + str(NUM_WORKERS[workdays[day]]))
  print(allocation)

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
    # print("Location: " + locations[location] + str(location_transacs)) # DEBUGGING
    workers = allocated_workers_day[workdays[day]][location]
    allocated_hours = apportionment(location_transacs, (10 * workers + 17 * NUM_CLASSIFIED[LOCATIONS[location]]))
    apportionment_at_location[location] = allocated_hours # saves allocation data to the location
    # print("Location: " + LOCATIONS[location] + " on " + workdays[day] + "\n" + str(allocated_hours)) # DEBUGGING
    # FOR GENERATING HISTOGRAM DATA (for generating data on the appropriate time range for histograms)
    full_hours_apport = [0] * len(location_hours)
    for i in range(len(allocated_hours)):
      full_hours_apport[idx_open + i] = allocated_hours[i] / (10/4)
    print("Location: " + LOCATIONS[location] + " on " + workdays[day] + "\n" + str(full_hours_apport))

  apportionment_data[day] = apportionment_at_location # saving the day to the apportionment 3D array

# DEBUGGING CODE
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
        scores_at_bucket.append(SCORES[shift_idx])
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

  # Objective function - max sum of all decision variables
  obj = p.lpSum(classified_vars)
  for i in range(len(dec_var)):
    obj += p.lpSum(np.dot(dec_var[i], shift_scores[i]))
  model += obj

  # constraint definitions
  # *  at least 2 people working at any given time
  # *  when num_workers + classified workers > 5, make at least 2 people present, otherwise make at least 1 person present
  min_workers = 1
  if num_workers + classified_amt > 5 and lp_name[:2] != "PS":
    # make at least 2 people present at each time
    min_workers = 2

  for bucket_idx in range(len(active_workers)):
    constraint = (p.lpSum(active_workers[bucket_idx]) >= min_workers, "Min workers at " + str(work_hours[bucket_idx]))
    model += constraint

  # increase minimum number of working for a given timeslot based on the timeslot's demand
  min_apportionment = [(apportionment[i] / (10 / 4)) for i in range(len(apportionment))]
  # DEBUGGING CODE
  # print("length of active workers arr: " + str(len(active_workers)))
  # print("length of apportionment data: " + str(len(max_apportionment)))
  for bucket_idx in range(len(active_workers)):
    if bucket_idx != 0 and bucket_idx != (len(active_workers) - 1):
      model += (p.lpSum(active_workers[bucket_idx]) >= min_apportionment[bucket_idx - 1], "Rec. min workers at " + str(work_hours[bucket_idx]))
  # sum of all classified shifts must equal num classified at location
  model += (p.lpSum(classified_vars) == classified_amt, "Req. amount Classified")

  # sum of all decision variables must equal allocated workers at location
  all_workers = p.lpSum(classified_vars)
  for bucket in dec_var:
    all_workers += p.lpSum(bucket)
  model += (all_workers == num_workers + classified_amt, "Worker limit")

  # solves the model
  status = model.solve()
  # print(status)
  # prints out the resulting decision variables FOR DEBUGGING
  # for var in model.variables():
  #   print(str(var) + ": " + str(p.value(var)))
  # for name, constraint in model.constraints.items():
  #   print(f"{name}: {constraint.value()}")
  return model

# SMALL TEST CASE FOR DEBUGGING
# print(staff_hrs["Mon"])
# print(allocated_workers_day["Mon"][4])
# scheduler(apportionment_data[0][4], allocated_workers_day["Mon"][4], staff_hrs["Mon"]["MS"], NUM_CLASSIFIED["MS"], "MS_Mon")

# loop containing the way to solve all LPs
for day_idx in range(len(workdays)):
  weekday = workdays[day_idx]
  print(weekday)
  for location_idx in range(len(LOCATIONS)):
    location = LOCATIONS[location_idx]
    print(location)
    model = scheduler(apportionment_data[day_idx][location_idx], allocated_workers_day[weekday][location_idx], \
      staff_hrs[weekday][location], NUM_CLASSIFIED[location], location + "_" + weekday)
    f = open("schedules/" + location + "_" + weekday + ".txt", "w")
    for var in model.variables():
      # writes to file the variables that are non-zero
      if var.value() > 0:
        f.write(str(var) + ": " + str(p.value(var)) + "\n")
    f.close()
