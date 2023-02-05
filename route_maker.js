
const { MongoClient } = require('mongodb')

function getDatabase(){
  const CONNECTION_STRING = "mongodb+srv://viewBusses:QUm3dDDHTDrdwW7k@cluster0.cana0cv.mongodb.net/test?retryWrites=true&w=majority";
  const client = new MongoClient(CONNECTION_STRING, { useNewUrlParser: true });
  var db = client.db("mydatabase");
  return db.collection("buses").find({}).toArray();
}

var database=getDatabase();

async function getRoute(fromt,tot,depT,arivT) {
  var data = await database;

  if(depT===0&&arivT===0){

    if(fromt===""){
      if(tot===""){
        return data;
      }
      return data.filter(function(tod){return tod.To===tot;});
    }else{
      if(tot===""){
        return data.filter(function(tod){return tod.From===fromt;});
      }
      return data.filter(function(tod){return tod.From===fromt&&tod.To===tot;});
    }

  }else if(depT===0&&arivT!==0){

    if(fromt===""){
      if(tot===""){
        return data.filter(function(tod){return tod.Arrival<arivT;});
      }
      return data.filter(function(tod){return tod.To===tot&&tod.Arrival<arivT;});
    }else{
      if(tot===""){
        return data.filter(function(tod){return tod.From===fromt&&tod.Arrival<arivT;});
      }
      return data.filter(function(tod){return tod.From===fromt&&tod.To===tot&&tod.Arrival<arivT;});
    }

  }else if(depT!==0&&arivT==0){

    if(fromt===""){
      if(tot===""){
        return data;
      }
      return data.filter(function(tod){return tod.To===tot&&tod.Departure>depT;});
    }else{
      if(tot===""){
        return data.filter(function(tod){return tod.From===fromt&&tod.Departure>depT;});
      }
      return data.filter(function(tod){return tod.From===fromt&&tod.To===tot&&tod.Departure>depT;});
    }

  }else{

    if(fromt===""){
      if(tot===""){
        return data.filter(function(tod){return tod.Arrival<arivT&&tod.Departure>depT;});
      }
      return data.filter(function(tod){return tod.To===tot&&tod.Arrival<arivT&&tod.Departure>depT;});
    }else{
      if(tot===""){
        return data.filter(function(tod){return tod.From===fromt&&tod.Arrival<arivT&&tod.Departure>depT;});
      }
      return data.filter(function(tod){return tod.From===fromt&&tod.To===tot&&tod.Arrival<arivT&&tod.Departure>depT;});
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
  var midroutes=[];
  midroutes[0]=[0,await soonestRoutesAnywhere(fromt,"",Ltime,0)];
  var solutions=await getRoute("",tot,0,0);
  //console.log(midroutes[0][1]);
  var tmp = midroutes[0][1].filter(function(route){for(var t=0;t<solutions.length;t++){if(solutions[t]._id===route._id){return true;}}return false;});
  //console.log(tmp);
  if(tmp.length>0){
    //console.log("Why?");
    return tmp;
  }

  for(var depth=1;depth<5;depth++){
    var tx=[];
    for(var route=1;route<midroutes[depth-1][1].length;route++){
      //console.log("Route: ",midroutes[depth-1][route][1]);
      tx.push([route,await soonestRoutesAnywhere(midroutes[depth-1][route][1]["To"],"",midroutes[depth-1][route][1]["Arrival"],0)]);

      //console.log(tx[route-1]);
      

      tmp = tx[route-1][1].filter(function(route){for(var t=0;t<solutions.length;t++){if(solutions[t]._id===route._id){return true;}}return false;});
      //console.log(tmp);
      if(tmp.length>0){
        console.log("Yay.",route);
        return tmp;
      }

    }
    midroutes[depth]=tx;
    console.log("Midroutes");
    console.log(tx);

    

  }

}

findRoute("Trigon","Laurel Ridge",780).then(value=>{console.log(value);});
//getRoute("HSC","",0,0).then(value=>{console.log(value);});

