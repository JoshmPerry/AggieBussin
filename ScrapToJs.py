### IMPORTS ###
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymongo

### BUS CLASS ###
class bus(object):

	def __init__(self,n1="Rev12"):
		self.name=n1
		self.trips=[]
		
	def addTrip(self,trip):
		"""stop should be a list with the first element as a string of the stop location
		and the second element another list of the stop times stored in military time"""
		self.trips+=[trip]
	
	def getName(self):
		return self.name

	def getTrips(self):
		return self.trips

	def getTrip(self,where):
		return self.trips[where]

	def getTripsLength(self):
		return len(self.trips)


def get_bus_schedule(root_web_URL, routes, local_path_to_webdriver ):

    bus_list=[]

    ### OPEN WEBSITE ###
    PATH_TO_WEBDRIVER = local_path_to_webdriver #"C:\\Users\\aweso\\OneDrive\\Documents\\hack\\chromedriver_win32\\chromedriver.exe"

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument("--disable-logging")
    options.add_argument('log-level=3')

    driver = webdriver.Chrome(PATH_TO_WEBDRIVER,options=options)

    ### GET THE ELEMENT ID FOR EACH TABLE ###
    bus_table_element_ids = []
    route_numbers = routes#{12,15,22,26,27,31,34,35,36,40,47,48, '47-48', 'N15'}
    for route_num in route_numbers:
        URL = root_web_URL + str(route_num)
        driver.get(URL)
        time.sleep(0.1)
        table_id = driver.find_element(By.CLASS_NAME,"timetable")
        #bus_table_element_ids += [table_id]
        
        bus_name = (table_id.find_element(By.CLASS_NAME, "Route")).text
        print("Currently Scrapping",bus_name)
        currentBus=bus(bus_name)
        location_id_code = "BGRouteColor RouteColorCompliment Route" + str(route_num)
        bus_stop_location_elements = (table_id.find_elements(By.TAG_NAME, "th"))[2:]
        bus_stops = []
        for element in bus_stop_location_elements:
            bus_stops += [(element.text).split(" - TO ")[0]]
        
        times_lr_ud_ids = table_id.find_elements(By.TAG_NAME, 'time')
        times_lr_ud = []
        for time_id in times_lr_ud_ids:
            timetext = time_id.text
            try:
                if(timetext[-1] == 'P'):
                    times_lr_ud += [((int((((timetext[:-1]).split(':')))[0])+12)*60 + (int(((timetext[:-1]).split(':'))[1])))]
                else:
                    times_lr_ud += [((int((((timetext[:-1]).split(':')))[0]))*60 + (int(((timetext[:-1]).split(':'))[1])))]
            except:
                None
        #print(times_lr_ud)

        #####################NEED TO CHANGE TYPE OF DATA FROM STOP BASED TO TRIP BASED#################################
        ###############################################################################################################
        n = len(bus_stops)
        for i in range(len(times_lr_ud)-1):
            if(i%n!=n-1):
                currentBus.addTrip([times_lr_ud[i],bus_stops[i%n],times_lr_ud[i+1],bus_stops[(i+1)%n]])
        
        bus_list += [currentBus]

    return bus_list
    

conn_str = "mongodb+srv://JoshmPerry:duPLYKDpBM11HfbB@cluster0.cana0cv.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client["mydatabase"]
collection = database["buses"]
routes={12,15,22,26,27,31,34,35,36,40,47,48, '47-48', 'N15',"01","01-04","03","03-05","04","05","06","07","08"}
URL='https://transport.tamu.edu/busroutes/Routes.aspx?r='
pathtoWebdriver="..\\chromedriver_win32\\chromedriver.exe"
print("Starting Uploading process...")
collection.drop()
for num,curbus in enumerate(get_bus_schedule(URL,routes,pathtoWebdriver)):
    print("Uploading",curbus.getName(),"to Database.",num)
    #print(curbus.getTrips())
    for num2,stop in enumerate(curbus.getTrips()):
        dictionaryToAdd={"_id":((num+1)*1000)+(1+num2),"BusName":curbus.getName(),"To":stop[3],"From":stop[1],"Arrival":stop[2]-2,"Departure":stop[0]-1}
        #print(dictionaryToAdd)
        collection.insert_one(dictionaryToAdd)
#collection.insert_one({"_id":1,"BusName":"Help me","To":"North Side","From":"South Side","Arrival":1500,"Departure":1450})

print("finished")

#bus = [[ariv,location1,depart],[ariv,location2,depart],[aric,location1,depart]]
#bus = [[]]

