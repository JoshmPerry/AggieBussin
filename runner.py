import pymongo
# Replace the uri string with your MongoDB deployment's connection string.
conn_str = "mongodb+srv://JoshmPerry:duPLYKDpBM11HfbB@cluster0.cana0cv.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client["mydatabase"]
collection = database["oplog.rs"]
#customers = database["customers"]
#customers.drop()
#collection.insert_one({"_id":1,"job":"Python"})

print(collection)
print("finished")

