import pymongo
import scraper.py

conn_str = "mongodb+srv://JoshmPerry:duPLYKDpBM11HfbB@cluster0.cana0cv.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client["mydatabase"]
collection = database["buses"]
routes={12,15,22,26,27,31,34,35,36,40,47,48, '47-48', 'N15'}
URL='https://transport.tamu.edu/busroutes/Routes.aspx?r='
pathtoWebdriver="..\\chromedriver_win32\\chromedriver.exe"


collection.drop()
for curbus in get_bus_schedule(URL,routes,pathtoWebdriver):
    dictionaryToAdd={"_id":curbus.getName().split()[0],"BusName":curbus.getName(),"Stops":curbus.getStops(),"Today":bool(curbus.getStops())}
    collection.insert_one(dictionaryToAdd)


print("finished")

