from sys import argv
from copy import deepcopy

def gen_timetable(t, classes, pos, excel_file, display_lectures, n):
    for i in range(len(classes[pos])):
        timetable = deepcopy(t)
        unit = classes[pos][i][0]
        type = classes[pos][i][2]
        if classes[pos][i][3] == "Monday":
            day = 1
        elif classes[pos][i][3] == "Tuesday":
            day = 2
        elif classes[pos][i][3] == "Wednesday":
            day = 3
        elif classes[pos][i][3] == "Thursday":
            day = 4
        elif classes[pos][i][3] == "Friday":
            day = 5
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
                gen_timetable(timetable, classes, pos + 1, excel_file, display_lectures, n)
            else:
                valid_timetable = False
                if n == 5:
                    valid_timetable = True
                    # excel_file.append(timetable)
                else:
                    if n!= 5:
                        empty = [True, True, True, True, True]
                        for day in range(1, 6):
                            for timeslot in range(1, len(timetable), 2):
                                if(timetable[timeslot][day] != ""):
                                    empty[day - 1] = False
                                    break
                        if empty.count(False) <= int(n):
                            valid_timetable = True
                if valid_timetable:
                    if display_lectures:
                        for lecture in lectures:
                            unit = lecture[0]
                            type = lecture[1]
                            if lecture[2] == "Monday":
                                day = 1
                            elif lecture[2] == "Tuesday":
                                day = 2
                            elif lecture[2] == "Wednesday":
                                day = 3
                            elif lecture[2] == "Thursday":
                                day = 4
                            elif lecture[2] == "Friday":
                                day = 5
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
        files = []
        lectures = []
        all_classes = []
        lines = []
        for i in range(1,5):
            files.append(argv[i])
            f = open(files[i - 1] + ".csv", "r")
            f.readline()
            for line in f:
                x = line.split(",") # need to change commas in description
                start = int(x[4][0:2])
                end = int(x[4][-5:-3])
                duration = end - start
                if x[1].find("Lecture") != -1 or x[1].find("Workshop") != -1:
                    lectures.append([argv[i], x[2][:-3], x[3], start, end, duration]) # may add x[1] in to account for workshops
                else:
                    lines.append([argv[i], x[1], x[2][:-3], x[3], start, end, duration])
            f.close()

        display_lectures = True if argv[5]=="lec=y" else False
        flags = []
        d_flag = -1
        e_flag = -1
        a_flag = -1
        n_flag = -1
        g_flag = -1
        l_flag = -1

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
            elif flag[0] == "e" or flag[0] == "a" or flag[0] == "n":
                if flag[0] == "e":
                    e_flag = i - 6
                elif flag[0] == "a":
                    a_flag = i - 6
                else:
                    n_flag = i - 6

                flags.append(flag.split("="))
            else:
                print("Invalid flag")
                exit(0)


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
        timetable = deepcopy(template)

        excel_file = []

        n = 5 if n_flag == -1 else flags[n_flag][1]
        gen_timetable(timetable, classes, 0, excel_file, display_lectures, n)
        if(len(excel_file) == 0):
            print("Unable to generate any timetables with the given value of the n flag")
            exit(0)

        if(len(excel_file) == 1):
            print(str(len(excel_file)) + " potential timetable generated.")
        else:
            print(str(len(excel_file)) + " potential timetables generated.")


        f = open("timetables.csv", "w")
        for temp in excel_file:
            for line in temp:
                f.write(",".join(line) + "\n")
            f.write("\n")
        f.close()

    else:
        print("usage: timetable_scheduler.py [arg1] [arg2] ... [arg4] [flag1] ... [flagn]")
