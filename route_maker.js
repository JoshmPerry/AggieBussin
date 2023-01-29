
const { MongoClient } = require('mongodb')

let finalList = [];
let almostFinalList = [];
let reallyAlmostFinalList = [];

async function getDatabase() {
  const CONNECTION_STRING = "mongodb+srv://JoshmPerry:duPLYKDpBM11HfbB@cluster0.cana0cv.mongodb.net/test?retryWrites=true&w=majority";
  const client = MongoClient.connect(CONNECTION_STRING, { useNewUrlParser: true });
  var db = client.db("mydatabase");
  return (db.collection("buses")).find().sort({ id: 1 });
}

const cursor = getDatabase();
const list4 = cursor.toArray();

for (let item of list4) {
  const list3 = Object.values(item);
  almostFinalList = almostFinalList.concat(list3);
}

for (let i = 0; i < almostFinalList.length; i += 3) {
  reallyAlmostFinalList.push([almostFinalList[i], almostFinalList[i + 1], almostFinalList[i + 2]]);
}

for (let i = 0; i < reallyAlmostFinalList.length; i++) {
  if (reallyAlmostFinalList[i][2].length === 0 || reallyAlmostFinalList[i][2][0][0] === 0) {
    continue;
  } else {
    finalList.push(reallyAlmostFinalList[i]);
  }
}

let stopsToday = new Set();
for (let i = 0; i < finalList.length; i++) {
  const stops = finalList[i][2];
  for (let j = 0; j < stops.length; j++) {
    stopsToday.add(stops[j][1]);
  }
}
stopsToday = Array.from(stopsToday);

function getStopsToday() {
  return stopsToday;
}
function find_bus_for_stops(locationA, locationB, list2) {
    let best_time = 600;
    let best_bus = "NOPE";
    let best_depart_time = 0;
    for (let i = 0; i < list2.length; i++) {
        let bus = list2[i];
        let bus_stops = [];
        // gather the valid bus stops
        for (let j = 0; j < bus[2].length; j++) {
            let element = bus[2][j];
            if (element[0] !== 0) {
                bus_stops.push(element);
            }
        }
        // check the stops until location A is found
        let start_index = -1;
        for (let i = 0; i < bus_stops.length; i++) {
            if (bus_stops[i][1] === locationA) {
                start_index = i;
                break;
            }
        }
        let end_index = -1;
        if (start_index >= 0) {
            for (let i = 0; i < bus_stops.length; i++) {
                if (bus_stops[i][1] === locationB) {
                    end_index = i;
                    break;
                }
            }
        }
        let time = 600;
        if (start_index !== -1 && end_index !== -1) {
            time = bus_stops[end_index][0] - bus_stops[start_index][2];
        }
        if (time < best_time && time > 0) {
            best_time = time;
            best_bus = bus[1];
            best_depart_time = bus[2][start_index][0];
        }
    }
    return [best_bus, best_depart_time, best_time];
}

print(find_bus_for_stops("Trigon","Deacon - West",finalList)[0])

// const mongo = require('mongodb');
// const MongoClient = mongo.MongoClient
// const url = "mongodb+srv://JoshmPerry:duPLYKDpBM11HfbB@cluster0.cana0cv.mongodb.net/test?retryWrites=true&w=majority"
// MongoClient.connect(url, {useNewUrlParser: true }, (err, client) => {
//     if (err) throw err;

//     var list4 = [];
//     const db = client.db("mydatabase");
//     db.listCollections().toArray().then((docs) => {docs.forEach((doc, idx, array) => {list4 += doc});});}).catch((err) => {}).finally(() => {client.close();});
//     cursor = (client.db("buses")).find().sort("_id")
//     client.close();

//     console.log(list4)
    

