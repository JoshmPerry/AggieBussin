from pymongo import MongoClient


final_list = []
almost_final_list = []
really_almost_final_list = []

def get_database():
    CONNECTION_STRING = "mongodb+srv://JoshmPerry:duPLYKDpBM11HfbB@cluster0.cana0cv.mongodb.net/test?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client['mydatabase']

database = get_database()


cursor = (database["buses"]).find().sort("_id")

list4 = list(cursor)
for item in list4:
    list3 = dict(item).values()
    almost_final_list += list(list3)

for i in range(0, len(almost_final_list), 3):
    really_almost_final_list += [[ almost_final_list[i] , almost_final_list[i+1] ,  almost_final_list[i+2] ]]

for i in range(len(really_almost_final_list)):
    if len(really_almost_final_list[i][2]) == 0 or really_almost_final_list[i][2][0][0]==0:
        None
    else:
        final_list += [ really_almost_final_list[i] ]


stops_today = set()
for i in range(len(final_list)):
    stops = final_list[i][2]
    for i in range(len(stops)):
        stops_today.add(stops[i][1])
stops_today = list(stops_today)


# for line in really_almost_final_list:
#     print(line)

# for bus in bus_list:
#     if len(bus['Stop']) == 0:
#         None
#     else:
#         almost_final_list += [bus]

# for bus in almost_final_list:


list1 = final_list


# for bus in final_list:
#     print(bus)


# list1 = [
#     [0, 'busname1', [  [999,'Loc1',1000],  [1009,'Loc2',1010],  [1019,'Loc3',1020],  [1029,'Loc4',1030],  [1039,'Loc1',-1]  ]],
#     [1, 'busname2', [  [999,'Loc2',1000],  [1009,'Loc3',1010],  [1019,'Loc4',1020],  [1029,'Loc1',1030],  [1039,'Loc2',-1]  ]],
#     [2, 'busname3', [  [999,'Loc3',1000],  [1009,'Loc4',1010],  [1019,'Loc1',1020],  [1029,'Loc2',1030],  [1039,'Loc3',-1]  ]],
#     [3, 'busname4', [  [999,'Loc4',1000],  [1009,'Loc1',1010],  [1019,'Loc2',1020],  [1029,'Loc3',1030],  [1039,'Loc4',-1]  ]]
#     ]


def get_stops_today():
    return stops_today


def find_bus_for_stops(locationA, locationB, list2):
    best_time = 600
    best_bus = "NOPE"
    best_depart_time = 0
    for i in range(len(list2)):
        bus = list2[i]
        # print(list2[i])
        bus_stops = []
        #gather the valid bus stops
        
        for j in range(len(bus[2])):
            element = bus[2][j]
            if(element[0] != 0):
                bus_stops += [element]
        
        # check the stops until location A is found
        start_index = -1
        # print(len(bus_stops))
        for i in range(len(bus_stops)):
            # print(stop1)
            if (bus_stops[i][1] == locationA):
                start_index = i
                break

        end_index = -1
        if(start_index >= 0):
            for i in range(len(bus_stops)):
                # print(bus_stops[i])
                if (bus_stops[i][1] == locationB):
                    end_index = i
                    break

        time = 600
        if(start_index != -1 and end_index != -1):
            time = bus_stops[end_index][0] - bus_stops[start_index][2]
        
        if(time < best_time and time > 0):
            best_time = time
            best_bus = bus[1]
            best_depart_time = bus[2][start_index][0]
        
    return [best_bus, best_depart_time, best_time]


# while True:
#     x = find_bus_for_stops(input("enter the start location: "),input("enter destination: "),list1)
#     print("Bus:", x[0], "    Departure time:",str(x[1]//60)+":"+str(x[1]%60),"    Travel time:", x[2])
