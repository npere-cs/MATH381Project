# Balanced Labor Modeling at UW HFS Cafes

<hr>

## Overview
This project contains the data and program necessary to determine the optimal scheduling of employees across University of Washington Cafes.

### Background
Managers of retail cafe establishments often have to balance the amount of workers that
they have at their disposal across all the locations they have authority over. Scheduling the
appropriate amount of employees at the multiple locations is often a difficult task to
undertake especially when there are so many factors that might impact the feasibility of
assignment. Factors such as limits on employee capacity, hours of operation, as well as trends
in customer demand must be considered to make an effective decision at creating a balanced
work schedule. Throughout each day there are varying amounts of customers that make
transactions; there are periods where very few customers come in, and there are times where
customers come in non-stop.

Existing decision making processes result in some locations typically seeing too many 
employees, where the low influx of customers does not justify the amount of workers present at
that moment. Conversely it is also a common occurrence that some other locations have too few
employees juggling tasks and serving a large number of customers without breaks. As such it is
best to balance out staffing appropriate for the customer demand as well as the well-being of
the employees.

### Goal
The goal of this project is to produce a balanced schedule of employee shifts across all UW Cafe locations which minimizes discrepancies between available service and customer demand at each location adhering to lower and upper limits on employee presence at each location and accommodating minimum time constraints on each shift.

<hr>

## Contents

### Data
Contains the relevant data used to obtain the optimal schedules. In particular, it has the data sets of transactional data at each location
obtained over a period of roughly 2 months.

### Graphs
Contains the histograms of average transactional data at each location on each day, see the [notation section](#schedules-1) to interpret the schedules.

### Schedules
Contains the optimal schedules at each location on each day of the week in plain text.

### Program Files
Contains the python program that encodes the mathematical model.
*  `parsing.py` - contains data processing for the data sets
*  `histograms.py` - contains program to generate histograms of average transactional data
*  `model.py` - contains the model used to determine the optimal schedules

<hr>

## Basic Notation
Below are the definitions for the various notation that is found as part of the model.

### Locations
*  By George - "BG"
*  Evolutionary Grounds - "EG"
*  Husky Grind - "HG"
*  Mary Gates Hall Espresso - "MG"
*  Microsoft Cafe - "MS"
*  Orin's Place - "OP"
*  Overpass Espresso - "OV"
*  Parnassus - "PS"

### Schedules
Have the following format for regular positions: `Start: HH:MM Shift: H:MM: X`
*  `Start: HH:MM` - Time of day that the shift starts
*  `Shift: H:MM` - Length of the shift
*  `X` - Number of employees starting at that time with the partiuclar shift length

Union positions take the following format: `Start: HH:MM: X`
*  `Start: HH:MM` - Time of day that the union position has the shift start
*  `X` - Number of union employees starting at that time
*  No shift length is specified here, as this type of position has a mandatory fixed length of 8.5 hours



## References

## Acknowledgements
*  Jon Biltucci - Assistant Director, Retail Dining UW HFS
*  Sara Billey - Professor of Mathematics at the University of Washington
*  Vasily Ilin - UW Dept. of Mathematics Graduate Student &amp; Teaching Assistant
*  University of Washington Housing &amp; Food Services
*  University of Washington Department of Mathematics

<hr>

&copy; 2022 Jonathan Kwan, Bill Li, Nickolay Perezhogin