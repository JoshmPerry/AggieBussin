
const { MongoClient } = require('mongodb')

function getDatabase(fromt,tot) {
  const CONNECTION_STRING = "mongodb+srv://viewBusses:QUm3dDDHTDrdwW7k@cluster0.cana0cv.mongodb.net/test?retryWrites=true&w=majority";
  const client = new MongoClient(CONNECTION_STRING, { useNewUrlParser: true });
  var db = client.db("mydatabase");
  if(fromt===""){
  if(tot===""){
    return db.collection("buses").find({}).toArray();
  }
  return db.collection("buses").find({to:tot}).toArray();
}else{
  if(tot===""){
    return db.collection("buses").find({from:fromt}).toArray();
  }
  return db.collection("buses").find({from:fromt,to:tot}).toArray();
}
}
getDatabase().then(value=>{console.log(value);});


