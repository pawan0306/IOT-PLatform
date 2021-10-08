import API
import math
import os

def calculate_dist(gps, iiit_loc):
	return math.sqrt( (float(gps[0])-float(iiit_loc[0]))**2 + (float(gps[1])-float(iiit_loc[1]))**2 )

barricades = [[20.34535, 41.34234], [18.42342, 35.45453], [24.42342, 56.45453], [27.42342, 60.45453], [10.42342, 21.45453]]
 
api = API.sensorapi()

min_dist = 5

while True:
	gps = api.getData("GPS")["data"][0]
	#print("Algo4a", gps)
	#for i in gps:
	for b in barricades:
		length = calculate_dist(gps[1], b)
		#print(length)
		if length < min_dist:
			#print("Min Dist")
			PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
			filepath = os.path.join(PARENT_DIR, "EmailService.py")
			api.trigger(filepath)
