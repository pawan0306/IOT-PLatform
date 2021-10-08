import os
from commAPI import obj
import json
 
class sensorapi(object): 

    def __init__(self):
        self.sensor = {}
        self.emailID = ''
        self.outputfile = ''
        self.binder()

    def binder(self):
        PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(PARENT_DIR, "conf.json")
        #print(os.path.dirname(os.path.abspath(__file__)))
        with open(filepath, "r") as f:
            data = json.loads(f.read())
            #print(data)
            #print(os.getcwd())
            #for i in data.keys():
            self.sensor = data['sensors']
            self.userID = data['userID']
            self.emailID = obj.getEmailID(self.userID)
            self.outputfile = data['outputfile']

    def getData(self, sensor):
        return obj.getData(self.sensor[sensor])
        
    def setData(self, index, sensor, value):
        return obj.setData(self.sensor[sensor][index], value)
        
    def sendMail(self, msg):
        obj.sendMail(self.emailID, msg)

    def display(self, line):
        with open(self.outputfile, 'a') as f:
            f.write(line + '\n')

    def getEmailID(self):
        return self.emailID

    def trigger(self, path):
        obj.trigger(path)