'''
Assignment 2: Tropical storm tracking analytics, part 1
IS590PR. Last modified 1/23/19

Member 1: Gnanendra Reddy Tugu Yagama Reddy (grt4)
Membere 2: Srikanth Pendyala ((Sp22)

Gnanendra was responsible for calculating the below mentioned parts:
1.Storm system ID. Also show its name if it had one.
2 Date range recorded for the storm (show start date and end date).
3. The total pressure change in millibars. (highest minus lowest)
4. Total number of hurricane-level storms tracked per year

Srikanth was resposnsible for below mentioned parts:
1.The highest Maximum sustained wind (in knots) and when it first occurred (date & time).
2.The highest Maximum sustained wind (in knots) and when it first occurred (date & time).
3.How many times it had a “landfall”


The NOAA National Hurricane Center has several databases available. We’re going to work with a historical
one called “HURDAT2”. From http://www.nhc.noaa.gov/data/#hurdat we can download two data files (Pacific
and Atlantic) in a non-standard CSV/fixed-width format. The strangeness is due to the mixture of two
interrelated line formats, the lack of column headers, and many missing data values (-99 & -999). There are
accompanying PDFs on that same webpage that describe the data format in fine detail.
Download both HURDAT2 data files and the descriptive PDFs. Read through the PDFs and peruse the data files
to get familiar with the custom data structure.
This Assignment is Part 1. (Assignment 3 will build on this work)

You may work alone or in a team of two students (your choice). This will give you time to work on the
fundamentals for a week and to have some code review before we add some more difficulty to it in
Assignment 3.

OVERALL TIPS:
You’ll need to use strings, lists, and dictionaries (or the similar collections.Counter class instead
of dictionaries) and simple text file I/O for this program. Though not required (yet), if you can organize your
program into some useful custom functions instead of one monolithic script, do so.

For now, focus on writing a Python program to do these things:
1. Create a solution that does not read in or retain the entire data set in memory at once. The data is
already sorted chronologically on disk, so you can take advantage of that. An incremental algorithm
here is more memory efficient and theoretically unlimited in how much data it can handle. Many of
you want to learn about "Big Data" computing – one of the important concepts for that is incremental
processing. This means your program will need to release the detail rows for each storm from memory
before it proceeds to load the next storm.

2. As it processes both the files, it should compute and print out the following data for each storm:
a. Storm system ID. Also show its name if it had one.
b. Date range recorded for the storm (show start date and end date).
c. The highest Maximum sustained wind (in knots) and when it first occurred (date & time).
Don’t rely on finding a Record Identifier of value “W” for this, because not all storm records
have these. So, you must find the maximum numerically.
d. The total pressure change in millibars. (highest minus lowest)
e. How many times it had a “landfall”

3. After all the storm-specific output above, your program should output these aggregate SUMMARY
statistics, sorted chronologically, by year. Omit years that have no storms at all:
a. Total number of storms tracked per year.
b. Total number of hurricane-level storms tracked per year (not all storms reach hurricane
category). Note that you should use the maximum wind >= 64kts to determine this instead of
looking just for the “HU” Status. This is because of situations when a storm that strong was
labeled another possible status (e.g. “EX” or “LO”).
c. TIP. Check yourself: In 1851, there were 6 total storms, 3 of which reached hurricane level.
d. TIP. Be careful, a year might have some storms but ZERO hurricanes. Make sure those display
properly too.

'''

def main(Data_file):
    from datetime import datetime
    line = Data_file.readline()

    hdr_count = 0
    strm_count = 0
    hdr_dict = {}
    dtl_dict = {}
    pressure_min = 0
    pressure_max = 0
    Pressure_change = 0
    count = 0
    while line:
        # Check if its a storm header or not
        #if line[0:2].isalpha():
        if line.startswith("AL") or line.startswith("EP") or line.startswith("CP"):
            hdr_count = 1
            strm_count = 1
            # Print Storm system ID & name
            if line[19:28] == "UNNAMED":
                # print("Storm id: {}".format(line[0:8]))
                print("Storm id :" + line[0:8])
            else:
                # print("Storm id: {}".format(line[0:8]), "the name of the storm is:", line[19:28].strip())
                print("Storm id: " + line[0:8] + ", " + "the name of the the storm is: " + line[19:28].strip())

        # Counting the number of data lines under each storm header
            count = int(line[34:36].strip())
            landfall_count = 0

        # Checking for a data line
        if line[0:2].isnumeric():
            date_1 = line[0:8] + ' ' + line[10:14]
            if hdr_count == 1:
                if line[0:4] in hdr_dict:
                    hdr_dict[line[0:4]] += 1
                else:
                    hdr_dict[line[0:4]] = 1
                first_date = datetime.strptime(date_1, '%Y%m%d %H%M')
                last_date = datetime.strptime(date_1, '%Y%m%d %H%M')
                max_wind_speed = int(line[38:41].strip())
                max_wind_date = (date_1, '%Y%m%d %H%M')
                hdr_count = 0

            # Date Range calculation

            if last_date < datetime.strptime(date_1, '%Y%m%d %H%M'):
                last_date = datetime.strptime(date_1, '%Y%m%d %H%M')

            # Max wind speed calculation

            if max_wind_speed < int(line[38:41].strip()):
                max_wind_speed = int(line[38:41].strip())
                max_wind_date = datetime.strptime(date_1, '%Y%m%d %H%M')

            # Pressure change calculation
            # print(line[39:41])
            pressure = int(line[39:41].strip())
            if pressure < pressure_min:
                pressure_min = pressure
            elif pressure > pressure_max:
                pressure_max = pressure
                Pressure_change = int(pressure_max - pressure_min)

            # Landfall identification
            if line[16] == 'L':
                landfall_count += 1
            c = line[19:21]
            if int(line[39:41]) >= 64 and strm_count == 1:
                if line[0:4] in dtl_dict:
                    dtl_dict[line[0:4]] += 1
                else:
                    dtl_dict[line[0:4]] = 1
                strm_count = 0
            count -= 1

            if count == 0:
                print("The storm starts from {} and ends on {}".format(first_date, last_date))
                print("The highest Maximum sustained wind in knots is " + str(max_wind_speed) + " on the date:" + str(max_wind_date))
                print("Number of times of landfall:  {}".format(str(landfall_count)))
                print("Change in Pressure is : {Pressure_change}")

        line = Data_file.readline()

    for a in hdr_dict:
        print('Year: ', a, 'and', 'Number. of storms is', hdr_dict[a])

    for b in dtl_dict:
        print('Year: ', b, 'and', 'Number of hurricane storms is', dtl_dict[b])

    return


with open('D:\My Courses\PR - IS 590\Assignments\A2\\hurdat2-1851-2017-050118.txt', 'r') as Data_file:
    main(Data_file)

print(' The NEAPNortheast and North Central Pacific hurricane file processing starts now!!!')

with open('D:\My Courses\PR - IS 590\Assignments\A2\\hurdat2-nepac-1949-2017-050418.txt','r') as Data_file:
    main(Data_file)


