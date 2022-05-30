results = {
  "2:00": 0,
  "2:30": 0,
  "3:00": 0,
  "3:30": 0,
  "4:00": 0,
  "4:30": 0,
  "5:00": 0
}
workdays = ["Mon", "Tue", "Wed", "Thu", "Fri"]
locations = ["BG", "EG", "HG", "MG", "MS", "OP", "OV", "PS"]
for day in workdays:
  for location in locations:
    f = open("schedules/text_schedules/" + location + "_" + day + ".txt", "r")
    assignments = f.read().split("\n")
    for line in assignments:
      if len(line) > 20:
        timeslot = line[20:24]
        count = line[26]
        results[timeslot] += int(count)
print(results)