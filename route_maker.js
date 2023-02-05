
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
        return db.collection("buses").find({Arrival:{$lt:arivT}}).toArray();
      }
      return db.collection("buses").find({To:tot,Arrival:{$lt:arivT}}).toArray();
    }else{
      if(tot===""){
        return db.collection("buses").find({From:fromt,Arrival:{$lt:arivT}}).toArray();
      }
      return db.collection("buses").find({From:fromt,To:tot,Arrival:{$lt:arivT}}).toArray();
    }

  }else if(depT!==0&&arivT==0){

    if(fromt===""){
      if(tot===""){
        return db.collection("buses").find({Departure:{$gt:depT}}).toArray();
      }
      return db.collection("buses").find({To:tot,Departure:{$gt:depT}}).toArray();
    }else{
      if(tot===""){
        return db.collection("buses").find({From:fromt,Departure:{$gt:depT}}).toArray();
      }
      return db.collection("buses").find({From:fromt,To:tot,Departure:{$gt:depT}}).toArray();
    }

  }else{

    if(fromt===""){
      if(tot===""){
        return db.collection("buses").find({Arrival:{$lt:arivT},Departure:{$gt:depT}}).toArray();
      }
      return db.collection("buses").find({To:tot,Arrival:{$lt:arivT},Departure:{$gt:depT}}).toArray();
    }else{
      if(tot===""){
        return db.collection("buses").find({From:fromt,Arrival:{$lt:arivT},Departure:{$gt:depT}}).toArray();
      }
      return db.collection("buses").find({From:fromt,To:tot,Arrival:{$lt:arivT},Departure:{$gt:depT}}).toArray();
    }
  }
}

async function soonestRoutes(fromt,tot,depT,arivT){
  var allroutes = await getRoute(fromt,tot,depT,arivT);
  var fastperbus=[];
  for (var x=0; x<allroutes.length;x++){
    var route = allroutes[x];
    var notlogged=true;
    for(var i=0;i<fastperbus.length;i++){
      if(route["BusName"]===fastperbus[i]["BusName"]){
        notlogged=false;
        if(route["Arrival"]<fastperbus[i]["Arrival"]){
          fastperbus[i]=route;
        }
      }
    }

    if(notlogged){
      //console.log(route);
      fastperbus.push(route);
    }


  }
  //for(time in fastperbus){console.log(fastperbus[time]["To"]);}
  return fastperbus;
}

async function soonestRoutesAnywhere(fromt,tot,depT,arivT){
  var allroutes = await getRoute(fromt,tot,depT,arivT);
  var fastperbus=[];
  for (var x=0; x<allroutes.length;x++){
    var route = allroutes[x];
    var notlogged=true;
    for(var i=0;i<fastperbus.length;i++){
      if(route["BusName"]===fastperbus[i]["BusName"]&&route["To"]===fastperbus[i]["To"]&&route["From"]===fastperbus[i]["From"]){
        notlogged=false;
        if(route["Arrival"]<fastperbus[i]["Arrival"]){
          fastperbus[i]=route;
        }
      }
    }

    if(notlogged){
      //console.log(route);
      fastperbus.push(route);
    }


  }
  //for(time in fastperbus){console.log(fastperbus[time]["To"]);}
  return fastperbus;
}

async function findRoute(fromt,tot,Ltime){
  var midman=await soonestRoutesAnywhere("",fromt,0,Ltime);
  var midroutes=[];
  for(var i=0;i<(midman).length;i++){
    //console.log(midman[i]);
    midroutes[i]=soonestRoutesAnywhere("",midman[i],0,midman[i]["Arrival"]);

  }

}

soonestRoutes("","MSC",799,0).then(value=>{console.log(value);});



