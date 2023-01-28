import pymongo
import scraper.py

conn_str = "mongodb+srv://JoshmPerry:duPLYKDpBM11HfbB@cluster0.cana0cv.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client["mydatabase"]
collection = database["buses"]




collection.drop()
for curbus in :
    dictionaryToAdd={"_id":curbus.getName().split()[0],"BusName":curbus.getName(),"Stops":curbus.getStops(),"Today":bool(curbus.getStops())}
    collection.insert_one(dictionaryToAdd)


print("finished")

