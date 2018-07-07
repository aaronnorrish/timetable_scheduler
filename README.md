# timetable_scheduler
A python program that generates all possible permutations of a timetable.

## Usage
This program may be run from the command line by using the following format:
  `python3 timetable_scheduler [file1] ... [file4] [flag1] ... [flagn]`
  
  Where `[file1]` is a string referencing the name of a CSV file containing the classes of a unit. Each line in the CSV file will be of the format:
  `[unit name] [activity] [other detail] [day] [time] [venue] [weeks]`
