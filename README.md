# timetable_scheduler
A python program that generates all possible permutations of a timetable.

## Usage
This program may be run from the command line by using the following format:

 ```
 python3 timetable_scheduler.py [file1] ... [file4] [lecflag] [flag1] ... [flagN]
 ```

  Where `[file1]` is the name of a CSV file containing the classes of a unit, `[lecflag]` denotes whether lectures should: not  clash with other classes (`lec=y`), be able to clash and display them in the timetable (`lec=d`) or be able to clash and don't display them (`lec=n`), and `[flag1]` is one of the below flags, in the form `<flag>=<value>`

  Note each line in the CSV file must be of the format:

 ```
 [unit name] [activity] [other detail] [day] [time] [venue] [weeks]
 ```

 ### Flags
 d - exclude all classes taking place on day d - may take multiple values, e.g `d=mon,thu`

 e - exclude all classes before the earliest time e

 a - exclude all classes after the latest time a

 n - exclude all timetables spanning greater than n days

 g - exclude all timetables with gaps greater than g hours between classes

 l - exclude all timetables with days with less than l hours of classes (only applies to days that have at least one class, i.e a timetable containing a day with no classes will not be excluded)

 Note times given with the above flags must be in 24 hour time and days must be given as the first three letters of the day in lowercase.

 ## Output
The number of timetables generated will be output to the command line or, if none were able to be generated, it will print "unable to generate any timetables with the given flags".

Each generated timetable is stored in "timetables.csv" and spans Monday to Friday, with times ranging from 8am to 6pm. Each timeslot is an hour long and represented as two cells - if a class falls on a timeslot, the first cell contains the unit to which the class belongs, and the second, the type of class it is (e.g Lecture). Timetables are separated by an empty row.

The number of hours per each type of class per week are also displayed in the csv file, on the first two lines to the right of the first timetable. 
