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
            bus_stops += [[0, (element.text).split(" - TO ")[0], 0]]
        
        times_lr_ud_ids = table_id.find_elements(By.TAG_NAME, 'time')
        times_lr_ud = []
        for time_id in times_lr_ud_ids:
            timetext = time_id.text
            try:
                if(timetext[-1] == 'P'):
                    times_lr_ud += [((int((t:=((timetext[:-1]).split(':')))[0])+12)*60 + (int(t[1])))]
                else:
                    times_lr_ud += [((int((t:=((timetext[:-1]).split(':')))[0]))*60 + (int(t[1])))]
            except:
                None
        print(times_lr_ud)

        #####################NEED TO CHANGE TYPE OF DATA FROM STOP BASED TO TRIP BASED#################################
        ###############################################################################################################


        for i in range(len(times_lr_ud)):
            n = len(bus_stops)
            if(i%n == 0 and i-1 >= 0): #if this is the first stop in the cycle, after the start of the day
                bus_stops[i%n][0] = times_lr_ud[i-1] #it has a special arrival time
            else: #on normal stops, arival is one minute prior to departure
                bus_stops[i%n][0] = times_lr_ud[i] - 1
            
            if(i%n == n-1): #if we are on the last stop in each cycle, but not end of day
                if (i+1 < len(times_lr_ud)): #if end of day
                    bus_stops[i%n][2] = -1 #bus at end of day does not depart
                else:
                    try:
                        bus_stops[i%n][2] = times_lr_ud[i+1]#bus does not depart until the next cycle
                    except:
                        bus_stops[i%n][2]=times_lr_ud[i]
            else:#otherwise the bus departs at the listed stop time
                bus_stops[i%n][2] = times_lr_ud[i]
            

        #print(bus_stops)

        for stop in bus_stops:
            currentBus.addTrip(stop)

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
    print("Uploading",curbus.getName(),"to Database.")
    #for num2,stop in enumerate(curbus.getStops()):
        #if(stop[0]!=0 or stop[2]!=0):
            #dictionaryToAdd={"_id":num*100+num2,"BusName":curbus.getName(),"Arrival":stop[0],"Departure":stop[2],"Location":stop[1]}
    dictionaryToAdd={"_id":num,"BusName":curbus.getName(),"Stop":curbus.getTrips()}
    collection.insert_one(dictionaryToAdd)


print("finished")

#bus = [[ariv,location1,depart],[ariv,location2,depart],[aric,location1,depart]]
#bus = [[]]

