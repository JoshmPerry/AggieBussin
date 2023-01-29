import pymongo
import scraper

conn_str = "mongodb+srv://JoshmPerry:duPLYKDpBM11HfbB@cluster0.cana0cv.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client["mydatabase"]
collection = database["buses"]
routes={12,15,22,26,27,31,34,35,36,40,47,48, '47-48', 'N15',"01","01-04","03","03-05","04","05","06","07","08"}
URL='https://transport.tamu.edu/busroutes/Routes.aspx?r='
pathtoWebdriver="..\\chromedriver_win32\\chromedriver.exe"

print("Starting Uploading process...")
collection.drop()
for num,curbus in enumerate(scraper.get_bus_schedule(URL,routes,pathtoWebdriver)):
    print("Uploading",curbus.getName(),"to Database.")
    #for num2,stop in enumerate(curbus.getStops()):
        #if(stop[0]!=0 or stop[2]!=0):
            #dictionaryToAdd={"_id":num*100+num2,"BusName":curbus.getName(),"Arrival":stop[0],"Departure":stop[2],"Location":stop[1]}
    dictionaryToAdd={"_id":num,"BusName":curbus.getName(),"Stop":curbus.getStops()}
    collection.insert_one(dictionaryToAdd)


print("finished")

#bus = [[ariv,location1,depart],[ariv,location2,depart],[aric,location1,depart]]
#bus = [[]]


