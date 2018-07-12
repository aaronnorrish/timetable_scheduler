from sys import argv
from copy import deepcopy

# Determines whether the timetable has classes on less than or equal to n days.
#   @param timetable a matrix representing a potential timetable
#   @param n an integer representing the maximum amount of days that classes may take place on
#   @return True if the timetable has classes on less than or equal to n days, False otherwise
def determine_used_days(timetable, n):
    empty = [True, True, True, True, True]
    for day in range(1, 6):
        for timeslot in range(1, len(timetable), 2):
            if(timetable[timeslot][day] != ""):
                empty[day - 1] = False
                break
    return empty.count(False) <= int(n)

# Determines whether the timetable has gaps between classes less than or equal to g hours.
#   @param timetable a matrix representing a potential timetable
#   @param g an integer representing the maximum number of hours allowed between classes
#   @return True if the timetable has gaps less than or equal to g hours, False otherwise
def det_g_flag(timetable, g): # need better testing
    for day in range(1, 6):
        class_started = False
        gap = False
        gap_duration = 0
        for timeslot in range(1, len(timetable), 2):
            if timetable[timeslot][day] != "" and not class_started:
                if gap:
                    if gap_duration > g:
                        return False
                    gap = False
                class_started = True
            elif timetable[timeslot][day] == "":
                if class_started:
                    gap = True
                    class_started = False
                if gap:
                    gap_duration += 1
    return True

# Determines whether the timetable has days with at least l hours of classes.
#   @param timetable a matrix representing a potential timetable
#   @param l an integer representing the minimum number of hours that classes may take up per day
#   @return True if the timetable has days with at least l hours of classes, False otherwise
def det_l_flag(timetable, l):
    for day in range(1, 6):
        duration = 0
        for timeslot in range(1, len(timetable), 2):
            if(timetable[timeslot][day] != ""):
                duration += 1
        if 0 < duration < l:
            return False
    return True

# Helper function that determines the corresponding integer for a given weekday.
#   @param day_string the weekday as a string
#   @return the corresponding integer to the input weekday
def get_day_num(day_string):
    if day_string == "Monday":
        day = 1
    elif day_string == "Tuesday":
        day = 2
    elif day_string == "Wednesday":
        day = 3
    elif day_string == "Thursday":
        day = 4
    elif day_string == "Friday":
        day = 5
    return day

# Recursive function used to generate all possible permutations of a time table.
#  If a class is found to clash or not meet a condition of the n, g or l flags
#  execution is terminated for that particular recursive branch.
#   @param t the current timetable table being generated from the previous step
#           in the recursive branch
#   @param classes a list containing all classes for all units (those that have met
#            the conditions of the d, e and a flags)
#   @param pos the current position in the classes list from which we must extract
#             a class from for the current instance of the timetable
#   @param excel_file a list containing all valid timetables
#   @param display_lectures a boolean denoting whether lectures should be displayed
#             in the timetable (True) or not (False)
#   @param n an integer representing the maximum amount of days that classes may take place on
#   @param g an integer representing the maximum number of hours allowed between classes
#   @param l an integer representing the minimum number of hours that classes may take up per day
def gen_timetable(t, classes, pos, excel_file, display_lectures, n, g, l):
    for i in range(len(classes[pos])):
        timetable = deepcopy(t)
        unit = classes[pos][i][0]
        type = classes[pos][i][2]
        day = get_day_num(classes[pos][i][3])
        time = (int(classes[pos][i][4]) - 8) * 2 + 1
        duration = int(classes[pos][i][6])
        clash = False
        for x in range(duration):
            if(timetable[time + x * 2][day] == ""):
                timetable[time + x * 2][day] = unit
                timetable[time + 1 + x * 2][day] = type
            else:
                clash = True
        if not clash:
            if pos != len(classes) - 1:
                gen_timetable(timetable, classes, pos + 1, excel_file, display_lectures, n, g, l)
            else:
                valid_timetable = True
                if n != 5 or g >= 0 or l > 0: # n, g or l flags used
                    if n != 5: # n flag used
                        valid_timetable = determine_used_days(timetable, n)
                    if valid_timetable and g >= 0: # g flag used
                        valid_timetable = det_g_flag(timetable, g)
                    if valid_timetable and l > 0: # l flag used
                        valid_timetable = det_l_flag(timetable, l)
                if valid_timetable:
                    if display_lectures:
                        for lecture in lectures:
                            unit = lecture[0]
                            type = lecture[1]
                            day = get_day_num(lecture[2])
                            time = (int(lecture[3]) - 8) * 2 + 1
                            duration = int(lecture[5])
                            for x in range(duration):
                                if(timetable[time + x * 2][day] == ""):
                                    timetable[time + x * 2][day] = unit
                                    timetable[time + 1 + x * 2][day] = type
                                else:
                                    timetable[time + x * 2][day] = timetable[time + x * 2][day] + "/" + unit
                                    timetable[time + 1 + x * 2][day] = timetable[time + 1 + x * 2][day] + "/" + type
                    excel_file.append(timetable)



if __name__ == '__main__':
    if(len(argv)) >= 6:
        # parse each unit's csv file
        files = []
        lectures = []
        lines = []
        include_lectures = True if argv[5]=="lec=y" else False
        for i in range(1,5):
            files.append(argv[i])
            f = open(files[i - 1] + ".csv", "r")
            f.readline()
            for line in f:
                x = line.split(",") # need to change commas in description
                start = int(x[4][0:2])
                end = int(x[4][-5:-3])
                duration = end - start
                if not include_lectures and (x[1].find("Lecture") != -1 or x[1].find("Workshop") != -1):
                    lectures.append([argv[i], x[2][:-3], x[3], start, end, duration])
                else:
                    lines.append([argv[i], x[1], x[2][:-3], x[3], start, end, duration])
            f.close()

        # parse command line flags
        display_lectures = True if argv[5]=="lec=d" else False
        flags = []
        d_flag, e_flag, a_flag, n_flag, g_flag, l_flag = -1, -1, -1, -1, -1, -1
        for i in range(6, len(argv)):
            flag = argv[i]
            invalid_flag = False
            if flag[0] == "d":
                d_flag = i - 6
                flag_d = [flag.split("=")[0]]
                flag = flag.split("=")[1].split(",")
                for f in flag:
                    if f == "mon" or f == "tue" or f == "wed" or f == "thu" or f == "fri":
                        flag_d.append(f)
                    else:
                        print("Invalid flag")
                        exit(0)
                flags.append(flag_d)
            elif flag[0] == "e" or flag[0] == "a" or flag[0] == "n" or flag[0]=="g" or flag[0] == "l":
                if flag[0] == "e":
                    e_flag = i - 6
                elif flag[0] == "a":
                    a_flag = i - 6
                elif flag[0] == "n":
                    n_flag = i - 6
                elif flag[0] == "g":
                    g_flag = i - 6
                else:
                    l_flag = i - 6
                flags.append(flag.split("="))
            else:
                print("Invalid flag")
                exit(0)

        # group all items in the lines list into classes
        all_classes = []
        for l in lines:
            # print(l)
            unit = l[0]
            type = l[1]
            number = l[2]
            found = False
            for c in all_classes:
                if c[0][0] == unit and c[0][1] == type and c[0][2] == number:
                    c.append(l)
                    found = True
                    break
            if not found:
                all_classes.append([l])

        # alter the classes list to include only classes meeting the requirements
        # of the d, f and a flags
        classes = []
        for i in range(len(all_classes)):
            potential_classes = all_classes.pop()
            c = []
            for i in range(len(potential_classes)):
                if d_flag != -1 and potential_classes[i][3][0:3].lower() in flags[d_flag]:
                    continue
                if e_flag != -1 and potential_classes[i][4] < int(flags[e_flag][1]):
                    continue
                if a_flag != -1 and potential_classes[i][5] > int(flags[a_flag][1]):
                    continue
                c.append(potential_classes[i])
            if len(c) == 0:
                print("Unable to generate any timetables with the given flags")
                exit(0)
            classes.append(c)

        # for l in lectures:
        #     print(l)

        # generate the timetable template
        times = ["8:00 am", "9:00 am", "10:00 am", "11:00 am", "12:00 pm", "1:00 pm", "2:00 pm", "3:00 pm", "4:00 pm", "5:00 pm", "6:00 pm"]
        header = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        template = [header]
        for time in times:
            time_slot = [time]
            for i in range(0, len(header) - 1):
                time_slot.append("")
            template.append(time_slot)
            time_slot = []
            for i in range(0, len(header)):
                time_slot.append("")
            template.append(time_slot)
        timetable = deepcopy(template) # needed?

        # set appropriate values of n, g and l depending on if their flag has been used
        n = 5 if n_flag == -1 else flags[n_flag][1]
        g = -1 if g_flag == -1 else int(flags[g_flag][1])
        l = -1 if l_flag == -1 else int(flags[l_flag][1])

        # add all valid timetables to the excel_file list
        excel_file = []
        gen_timetable(timetable, classes, 0, excel_file, display_lectures, n, g, l)
        if(len(excel_file) == 0):
            print("Unable to generate any timetables with the given flags")
            exit(0)
        elif(len(excel_file) == 1):
            print(str(len(excel_file)) + " potential timetable generated.")
        else:
            print(str(len(excel_file)) + " potential timetables generated.")

        # write the timetables to the excel file
        f = open("timetables.csv", "w")
        for temp in excel_file:
            for line in temp:
                f.write(",".join(line) + "\n")
            f.write("\n")
        f.close()

    else:
        print("usage: timetable_scheduler.py [arg1] [arg2] ... [arg4] [lecflag] [flag1] ... [flagN]")
