import numpy as np
from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
model = LpProblem(name="Heuristic", sense=LpMinimize)
x = []
for i in range(0, 24):
  if (i < 10):
    x.append(LpVariable(name="x0"+str(i), lowBound=0, cat="Integer"))
  else:
    x.append(LpVariable(name="x"+str(i), lowBound=0, cat="Integer"))
for i in range(0, 6):
  model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 2, str(i)+":00")
for i in range(6, 10):
  model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 8, str(i)+":00")
for i in range(10, 12):
  model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 4, str(i)+":00")
for i in range(12, 16):
  model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 3, str(i)+":00")
for i in range(16, 18):
  model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 6, str(i)+":00")
for i in range(18, 22):
  model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 5, str(i)+":00")
for i in range(22, 24):
  model += (x[i] + x[i-1] + x[i-2] + x[i-3] + x[i-5] + x[i-6] + x[i-7] + x[i-8] >= 3, str(i)+":00")
model += lpSum(sum(x))
status = model.solve()
print(model)
print(f"status: {model.status}, {LpStatus[model.status]}")
print(f"objective: {model.objective.value()}")
for var in model.variables():
  print(f"{var.name}: {var.value()}")
print()
for name, constraint in model.constraints.items():
  print(f"{name}: {constraint.value()}")