# timetable_scheduler
A python program that generates all possible permutations of a timetable.

## Usage
This program may be run from the command line by using the following format:
  
 `python3 timetable_scheduler [file1] ... [file4] [flag1] ... [flagN]`
  
  Where `[file1]` is the name of a CSV file containing the classes of a unit. Each line in the CSV file will be of the format:
  
 `[unit name] [activity] [other detail] [day] [time] [venue] [weeks]`

and `[flag1]` is one of the following flags, in the form `[<flag>=<value>]`
   
 ### Flags
 d - exclude all classes taking place on day d - may take multiple values, e.g `d=mon,thu`
 
 e - exclude all classes before the earliest time e
 
 l - exclude all classes after the latest time l 
 
 n - exclude all timetables spanning greater than n days
 
 Note times given with the above flags must be in 24 hour time and days must be given as the first three letters of the day in lowercase.
