from sys import argv
from copy import deepcopy

def gen_timetable(t, classes, pos, excel_file):
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
        for n in range(duration):
            if(timetable[time + n * 2][day] == ""):
                timetable[time + n * 2][day] = unit
                timetable[time + 1 + n * 2][day] = type
            else:
                clash = True
        if not clash:
            if pos != len(classes) - 1:
                gen_timetable(timetable, classes, pos + 1, excel_file)
            else:
                excel_file.append(timetable)

if __name__ == '__main__':
    if(len(argv)) == 5:
        files = []
        lectures = []
        classes = []
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
                if x[1] == "Lecture":
                    lectures.append([argv[i], x[2][:-3], x[3], start, end, duration])
                else:
                    lines.append([argv[i], x[1], x[2][:-3], x[3], start, end, duration])
            f.close()

        for l in lines:
            unit = l[0]
            type = l[1]
            number = l[2]

            found = False
            for c in classes:
                if c[0][0] == unit and c[0][1] == type and c[0][2] == number:
                    c.append(l)
                    found = True
                    break
            if not found:
                classes.append([l])

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
        gen_timetable(timetable, classes, 0, excel_file)

        f = open("timetables.csv", "w")
        for temp in excel_file:
            for line in temp:
                f.write(",".join(line) + "\n")
            f.write("\n")
        f.close()

    else:
        print("usage: timetableScheduler.py [arg1] [arg2] ... [arg4]")
