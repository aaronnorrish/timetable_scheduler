# timetable_scheduler
A python program that generates all possible permutations of a timetable.

## Usage
This program may be run from the command line by using the following format:
  
 `python3 timetable_scheduler [file1] ... [file4] [lecflag] [flag1] ... [flagN]`
  
  Where `[file1]` is the name of a CSV file containing the classes of a unit, `[lecflag]` denotes whether lectures should: not  clash with other classes (`lec=y`), be able to clash and display them in the timetable (`lec=d`) or be able to clash and don't display them (`lec=n`), and `[flag1]` is one of the below flags, in the form `<flag>=<value>` 
  
  Note each line in the CSV file must be of the format:
  
 `[unit name] [activity] [other detail] [day] [time] [venue] [weeks]`




   
 ### Flags
 d - exclude all classes taking place on day d - may take multiple values, e.g `d=mon,thu`
 
 e - exclude all classes before the earliest time e
 
 a - exclude all classes after the latest time a 
 
 n - exclude all timetables spanning greater than n days
 
 g - exclude all timetables with gaps greater than g hours between classes
 
 l - exclude all timetables with days with less than l hours of classes (only applies to days that have at least one class, i.e a timetable containing a day with no classes will not be excluded)

 
 Note times given with the above flags must be in 24 hour time and days must be given as the first three letters of the day in lowercase.
