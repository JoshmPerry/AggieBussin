from flask import Flask, request
from flask import *
from flask_restful import Resource, Api
import sys
import os
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
port = 8080







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

print(final_list)

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

def findBusRoutesTo(location,Mlist):
    options=[]
    for stop in stops_today:
        stop=stop.split(" - TO")[0]
        if location!=stop:
            temp=find_bus_for_stops(stop,location,Mlist)
            if temp[0]!="NOPE":
                options+=[temp+[stop]]
    return options

def findBusRoutesFrom(location,Mlist):
    options=[]
    for stop in stops_today:
        stop=stop.split(" - TO")[0]
        if location!=stop:
            temp=find_bus_for_stops(location,stop,Mlist)
            if temp[0]!="NOPE":
                options+=[temp+[stop]]
    return options

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
allocations="<p>"
for stop in get_stops_today():
    allocations+="{stop}, ".format(stop=stop)
allocations=allocations[:-1]+"</p>\n"


if sys.argv.__len__() > 1:
    port = sys.argv[1]
print("Api running on port : {} ".format(port))

@app.route("/bus", methods=["GET", "POST"])
def adder_page():
    errors = ""
    if request.method == "POST":
        number1 = None
        number2 = None
        locations=get_stops_today()
        number1 = request.form["number1"]
        if not number1 in locations and number2!="":
            errors += "<p>{!r} is not a valid location for today.</p>\n".format(request.form["number1"])
        
        number2 = request.form["number2"]
        if not number2 in locations and number2!="":
            errors += "<p>{!r} is not a valid location for today.</p>\n".format(request.form["number2"])

        if number1 in locations and number2=="":
            toGoWhere=findBusRoutesFrom(number1,list1)
            routes="<p>These are the bus rides from {loc}:</p>\n".format(loc=number1)
            for place in toGoWhere:
                ArrivHour=int(place[1]/60)
                ArrivMin=place[1]%60
                routes+="<p>There is a ride to {loc} at {ArrivHour}:{ArrivMin} lasting {time} minutes on bus {bus}<p>".format(loc=place[3],time=place[2],bus=place[0],ArrivHour=ArrivHour,ArrivMin=ArrivMin)
            return '''
                    <html>
                        <body>
                            {routes}
                            <p><a href="/">Click here to find another bus route.</a>
                        </body>
                    </html>
                '''.format(routes=routes)


        if number2 in locations and number1=="":
            toGoWhere=findBusRoutesFrom(number2,list1)
            routes="<p>These are the bus rides to {loc}:</p>\n".format(loc=number2)
            for place in toGoWhere:
                ArrivHour=int(place[1]/60)
                ArrivMin=place[1]%60
                routes+="<p>There is a ride from {loc} at {ArrivHour}:{ArrivMin} lasting {time} minutes on bus {bus}<p>".format(loc=place[3],time=place[2],bus=place[0],ArrivHour=ArrivHour,ArrivMin=ArrivMin)
            return '''
                    <html>
                        <body>
                            {routes}
                            <p><a href="/">Click here to find another bus route.</a>
                        </body>
                    </html>
                '''.format(routes=routes)


        if number1 in locations and number2 in locations:
            
            result = find_bus_for_stops(number1,number2,list1)
            if result[0]=="NOPE":
                errors +="<p>{loc1} to {loc2} is not a possible route taking a single bus</p>\n".format(loc1=number1,loc2=number2)
            else:
                ArrivHour=int(result[1]/60)
                ArrivMin=result[1]%60
                return '''
                    <html>
                        <body>
                            <p>You should take {result[0]} bus at {ArrivHour}:{ArrivMin}.</p>
                            <p>It will take roughly {result[2]} minutes to arrive at your destination.</p>
                            <p><a href="/">Click here to find another bus route.</a>
                        </body>
                    </html>
                '''.format(result=result,ArrivHour=ArrivHour,ArrivMin=ArrivMin)


    #return render_template("index.html"),# data=data)
    return '''
        <html>
            <body>
                <p>Locations:</p>
                {stops}
                {errors}
                <p>Enter your current location:</p>
                <form method="post" action=".">
                    <p><input name="number1" /></p>
                    <p>Enter your destination:</p>
                    <p><input name="number2" /></p>
                    <p><input type="submit" value="Find bus route" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors,stops=allocations)