#!/usr/bin/env python3

import schedule 
import time 
import threading 
import json
from kafka import KafkaConsumer, KafkaProducer
import random
from datetime import datetime, timedelta
from datetime import date
import calendar
import sys

sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm

week_dict = {0:"Monday",1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}

class Scheduler:

    def __init__(self,dataDc):

        self.dataDc=dataDc
        self.uid_job = None
        self.uid_job_dict = {}

    def passMetadata(self):
        pass

    def job_done(self, arg):
        uname,app_id,end_time,uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd= arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6],arg[7],arg[8],arg[9],arg[10],arg[11]
        print("injobdone")
        msg = {
                "action":"stop",
                    "jID": str(to_snd),
                    "placeholder":str(placeholder),
                    "location":str(location),
                    "appID":str(app_id),
                    "algoID":str(algoID),
                    "sensorList":sensorList,
                    "userID":str(uname),
                    "devID":str(devID),
                    "RAM":str(RAM),
                    "CPU":str(CPU)
                    }
        cm.send_message("DP",msg)
        print(self.uid_job_dict[uid_job])
        schedule.cancel_job(self.uid_job_dict[uid_job])
        print("job_done")

    def job_done_interval(self, arg):
        uname,app_id,end_time,uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd= arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6],arg[7],arg[8],arg[9],arg[10],arg[11]
        print("injobdone")
        msg = {
                "action":"stop",
                    "jID": str(to_snd),
                    "placeholder":str(placeholder),
                    "location":str(location),
                    "appID":str(app_id),
                    "algoID":str(algoID),
                    "sensorList":sensorList,
                    "userID":str(uname),
                    "devID":str(devID),
                    "RAM":str(RAM),
                    "CPU":str(CPU)
                    }
        cm.send_message("DP",msg)
        print(self.uid_job_dict[uid_job])
        # schedule.cancel_job(self.uid_job_dict[uid_job])
        print("job_done")
        

    def schedule_on_days_interval(self,arg):
        uname,app_id,end_time,uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd= arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6],arg[7],arg[8],arg[9],arg[10],arg[11]
        print("in_schedule_on_days")
        msg = {
            "action":"start",
                "jID": str(to_snd),
                "placeholder":str(placeholder),
                "location":str(location),
                "appID":str(app_id),
                "algoID":str(algoID),
                "sensorList":sensorList,
                "userID":str(uname),
                "devID":str(devID),
                "RAM":str(RAM),
                "CPU":str(CPU)
                }

        #cm.send_message("DP",msg)
        #print("message_sent")
        
        job_id = schedule.every().day.at(end_time).do(self.job_done_interval,((uname,app_id,end_time,uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd))) 
        #print(job_id)


    def schedule_on_days(self,arg):
        uname,app_id,end_time,uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd= arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6],arg[7],arg[8],arg[9],arg[10],arg[11]
        print("in_schedule_on_days")
        msg = {
            "action":"start",
                "jID": str(to_snd),
                "placeholder":str(placeholder),
                "location":str(location),
                "appID":str(app_id),
                "algoID":str(algoID),
                "sensorList":sensorList,
                "userID":str(uname),
                "devID":str(devID),
                "RAM":str(RAM),
                "CPU":str(CPU)
                }

        cm.send_message("DP",msg)
        #print("message_sent")
        
        job_id = schedule.every().day.at(end_time).do(self.job_done,((uname,app_id,end_time,uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd))) 
        #print(job_id)

    def schedule_pending(self):
        while True:
            schedule.run_pending()
            time.sleep(1)   

    def run_thread(self):
        t1 = threading.Thread(target=self.schedule_pending()) 
        t1.start()
           
       
    def schedule_interval(self,arg):
        uname,app_id,end_time,uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd= arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6],arg[7],arg[8],arg[9],arg[10],arg[11]
        print("inscheduleinterval")
        msg = {
            "action":"start",
                "jID": str(to_snd),
                "placeholder":str(placeholder),
                "location":str(location),
                "appID":str(app_id),
                "algoID":str(algoID),
                "sensorList":sensorList,
                "userID":str(uname),
                "devID":str(devID),
                "RAM":str(RAM),
                "CPU":str(CPU)
                }
        cm.send_message("DP",msg)
        #print("in interval",self.uid_job_dict[uid_job])
        now = datetime.now()
        #print("interval",now)

        end_time = now + \
				timedelta(minutes=end_time)

        end_time = end_time.strftime("%H:%M:%S")

        #print(end_time)
        job_id = schedule.every().day.at(end_time).do(self.job_done_interval,((uname,app_id,end_time,uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd))) 
        # try:
        #     if(self.uid_job_dict[uid_job]):
        #         #print("we are in end interval")
        #         # schedule.cancel_job(self.uid_job_dict[uid_job])
        # except:
        #     pass
        # self.uid_job_dict[uid_job]=job_id
        
    def schedule_immediate(self,uname,app_id,end_time,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd):
        
        now = datetime.now()
        cur_time = now + \
            timedelta(seconds=1)

        cur_time = cur_time.strftime("%H:%M:%S")
        d = week_dict[datetime.today().weekday()]
        
        #print(d)
        #print((cur_time))
        if(d.lower()=="monday"):
            # self.uid_job += ";mon"
            job_id = schedule.every().monday.at(cur_time).do( self.schedule_on_days_interval,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
        elif(d.lower()=="tuesday"):
            # self.uid_job += ";tue"
            job_id = schedule.every().tuesday.at(cur_time).do( self.schedule_on_days_interval,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
        elif(d.lower()=="wednesday"):
            # self.uid_job += ";wed"
            job_id = schedule.every().wednesday.at(cur_time).do( self.schedule_on_days_interval,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
        elif(d.lower()=="thursday"):
            # self.uid_job += ";thu"
            job_id = schedule.every().thursday.at(cur_time).do( self.schedule_on_days_interval,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
        elif(d.lower()=="friday"):
            # self.uid_job += ";fri"
            job_id = schedule.every().friday.at(cur_time).do( self.schedule_on_days_interval,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
        elif(d.lower()=="saturday"):         
            # self.uid_job += ";sat"
            job_id = schedule.every().saturday.at(cur_time).do( self.schedule_on_days_interval,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
        elif(d.lower()=="sunday"):
            #print("helloooo")
            # self.uid_job += ";sun"
            job_id = schedule.every().sunday.at(cur_time).do( self.schedule_on_days_interval,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
        
        return job_id
    
    
    
    def startScheduling(self,dataDc):

        action = dataDc["action"]
        if(action == "stop"):
            stop_id = dataDc["jid"]
            msg = {
                 "action":"stop",
                "jID": str(stop_id),
                }
            cm.send_message("DP",msg)
            print(self.uid_job_dict[stop_id])
            schedule.cancel_job(self.uid_job_dict[stop_id])

        else:
            uname = dataDc["userID"]
            app_id = dataDc["appID"]
            algoID = dataDc["algoID"]
            placeholder = dataDc["placeholder"]
            location = dataDc["location"]
            action = dataDc["action"]
            sensorList = dataDc["sensorList"]
            devID = dataDc["devID"]
            RAM = dataDc["RAM"]
            CPU = dataDc["CPU"]
            scDc=dataDc["schedule"]
            priority=scDc["priority"]
            dayLst = scDc["days"]
            start_time = scDc["start_time"]
            end_time = scDc["end_time"]
            interval= scDc["interval"]
            duration=scDc["duration"]
            
            if(placeholder != ""):
                to_snd = placeholder+"_"+uname+"_"+app_id+"_"+algoID
            else:
                to_snd = location+"_"+uname+"_"+app_id+"_"+algoID

            
        




            request_type=scDc["request_type"]
            job_id = None
            if(placeholder != ""):
                self.uid_job = placeholder+"_"+uname+"_"+app_id+"_"+algoID
            else:
                self.uid_job = location+"_"+uname+"_"+app_id+"_"+algoID

            # self.uid_job = placeholder+";"+uname+";"+app_id+";"+algoID
            if request_type=="immediate":
                # self.uid_job += ";i"

                now = datetime.now()
                cur_time = now + \
                    timedelta(seconds=1)

                cur_time = cur_time.strftime("%H:%M:%S")
                d = week_dict[datetime.today().weekday()]
                
                #print(d)
                #print((cur_time))
                if(d.lower()=="monday"):
                    # self.uid_job += ";mon"
                    job_id = schedule.every().monday.at(cur_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                elif(d.lower()=="tuesday"):
                    # self.uid_job += ";tue"
                    job_id = schedule.every().tuesday.at(cur_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                elif(d.lower()=="wednesday"):
                    # self.uid_job += ";wed"
                    job_id = schedule.every().wednesday.at(cur_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                elif(d.lower()=="thursday"):
                    # self.uid_job += ";thu"
                    job_id = schedule.every().thursday.at(cur_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                elif(d.lower()=="friday"):
                    # self.uid_job += ";fri"
                    job_id = schedule.every().friday.at(cur_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                elif(d.lower()=="saturday"):         
                    # self.uid_job += ";sat"
                    job_id = schedule.every().saturday.at(cur_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                elif(d.lower()=="sunday"):
                    #print("helloooo")
                    # self.uid_job += ";sun"
                    job_id = schedule.every().sunday.at(cur_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                

                # job_id = self.schedule_immediate(uname,app_id,end_time,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)
                
                self.uid_job_dict[self.uid_job] = job_id
            else: # cron job
                if interval != "None":

                    end_time = int(duration)
                    now = datetime.now()
                    #print("interval",now)

                    end_time = now + \
                            timedelta(minutes=end_time)

                    end_time = end_time.strftime("%H:%M:%S")
                    job_id = self.schedule_immediate(uname,app_id,end_time,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)
                
                    self.uid_job_dict[self.uid_job] = job_id
                    # schObj.run_thread()
                    
                    end_time = int(duration)
                    #print(end_time)
                    # job_id = schedule.every().day.at(end_time).do(self.job_done_interval,((uname,app_id,end_time,uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd))) 
                           




                    # self.uid_job += ";n"
                    # end_time = int(duration)
                    job_id = schedule.every(int(interval)).minutes.do(self.schedule_interval,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                    # self.uid_job += ";n"+str(random.randint(0,10000))
                    self.uid_job_dict[self.uid_job] = job_id
                    #print("jobid",job_id)
                else:
                    if dayLst == 'everyday':
                        # self.uid_job += ";e"
                        #print("hi")
                        alllst = week_dict.values()
                        #print(alllst)
                        for d in alllst:
                            if(d.lower()=="monday"):
                                # self.uid_job += ";mon"
                                job_id = schedule.every().monday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                            elif(d.lower()=="tuesday"):
                                # self.uid_job += ";tue"
                                job_id = schedule.every().tuesday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                            elif(d.lower()=="wednesday"):
                                # self.uid_job += ";wed"
                                job_id = schedule.every().wednesday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                            elif(d.lower()=="thursday"):
                                # self.uid_job += ";thu"
                                job_id = schedule.every().thursday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                            elif(d.lower()=="friday"):
                                # self.uid_job += ";fri"
                                job_id = schedule.every().friday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                            elif(d.lower()=="saturday"):
                                # self.uid_job += ";sat"
                                job_id = schedule.every().saturday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                                
                            elif(d.lower()=="sunday"):
                                # self.uid_job += ";sun"
                                #print(start_time)
                                #print(uname,app_id,end_time,self.uid_job)
                                job_id = schedule.every().sunday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                            
                            self.uid_job_dict[self.uid_job] = job_id

                    else:
                        d = dayLst
                        # self.uid_job += ";dd"
                        if(d=="monday"):
                            # self.uid_job += ";mon"
                            job_id = schedule.every().monday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                        elif(d=="tuesday"):
                            # self.uid_job += ";tue"
                            job_id = schedule.every().tuesday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                        elif(d=="wednesday"):
                            # self.uid_job += ";wed"
                            job_id = schedule.every().wednesday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                        elif(d=="thursday"):
                            # self.uid_job += ";thu"
                            job_id = schedule.every().thursday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                        elif(d=="friday"):
                            # self.uid_job += ";fri"
                            job_id = schedule.every().friday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                        elif(d=="saturday"):
                            # self.uid_job += ";sat"
                            job_id = schedule.every().saturday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                            
                        elif(d=="sunday"):
                            # self.uid_job += ";sun"
                            #print(start_time)
                            #print(uname,app_id,end_time,self.uid_job)
                            job_id = schedule.every().sunday.at(start_time).do( self.schedule_on_days,((uname,app_id,end_time,self.uid_job,algoID,sensorList,devID,RAM,CPU,placeholder,location,to_snd)))
                        
                        self.uid_job_dict[self.uid_job] = job_id

            # t1 = threading.Thread(target=schObj.schedule_pending()) 
            # t1.start()
            # schObj.schedule_pending()
            schObj.run_thread()

          
# with open('user_config.json') as jf:
#     dataDc= json.load(jf)
##print(dataDc)

if __name__=="__main__":

    schObj=Scheduler(dataDc=None)
    t2 = threading.Thread(target=cm.consume_msg("AS",schObj.startScheduling)) 
    t2.start()
  
