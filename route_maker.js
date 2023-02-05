
const { MongoClient } = require('mongodb')

function getRoute(fromt,tot,depT,arivT) {
  const CONNECTION_STRING = "mongodb+srv://viewBusses:QUm3dDDHTDrdwW7k@cluster0.cana0cv.mongodb.net/test?retryWrites=true&w=majority";
  const client = new MongoClient(CONNECTION_STRING, { useNewUrlParser: true });
  var db = client.db("mydatabase");

  if(depT===0&&arivT===0){

    if(fromt===""){
      if(tot===""){
        return db.collection("buses").find({}).toArray();
      }
      return db.collection("buses").find({To:tot}).toArray();
    }else{
      if(tot===""){
        return db.collection("buses").find({From:fromt}).toArray();
      }
      return db.collection("buses").find({From:fromt,To:tot}).toArray();
    }

  }else if(depT===0&&arivT!==0){

    if(fromt===""){
      if(tot===""){
        return db.collection("buses").find({Arrival:{$gt:arivT}}).toArray();
      }
      return db.collection("buses").find({To:tot,Arrival:{$gt:arivT}}).toArray();
    }else{
      if(tot===""){
        return db.collection("buses").find({From:fromt,Arrival:{$gt:arivT}}).toArray();
      }
      return db.collection("buses").find({From:fromt,To:tot,Arrival:{$gt:arivT}}).toArray();
    }

  }else if(depT!==0&&arivT==0){

    if(fromt===""){
      if(tot===""){
        return db.collection("buses").find({Departure:{$lt:depT}}).toArray();
      }
      return db.collection("buses").find({To:tot,Departure:{$lt:depT}}).toArray();
    }else{
      if(tot===""){
        return db.collection("buses").find({From:fromt,Departure:{$lt:depT}}).toArray();
      }
      return db.collection("buses").find({From:fromt,To:tot,Departure:{$lt:depT}}).toArray();
    }

  }else{

    if(fromt===""){
      if(tot===""){
        return db.collection("buses").find({Arrival:{$gt:arivT},Departure:{$lt:depT}}).toArray();
      }
      return db.collection("buses").find({To:tot,Arrival:{$gt:arivT},Departure:{$lt:depT}}).toArray();
    }else{
      if(tot===""){
        return db.collection("buses").find({From:fromt,Arrival:{$gt:arivT},Departure:{$lt:depT}}).toArray();
      }
      return db.collection("buses").find({From:fromt,To:tot,Arrival:{$gt:arivT},Departure:{$lt:depT}}).toArray();
    }

  }



}

async function findRoute(fromt,tot,Ltime){
  var midman=await getRoute("",fromt,0,Ltime);
  var midroutes=[];
  for(var i=0;i<(midman).length;i++){
    //console.log(midman[i]);
    midroutes[i]=getRoute("",midman[i],0,midman[i]["Arrival"]);

  }

}

findRoute("","North Side",0,1499).then(value=>{console.log(value);});



