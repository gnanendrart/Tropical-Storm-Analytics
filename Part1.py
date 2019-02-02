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


