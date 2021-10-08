#!/usr/bin/env python3

import random
import time


class ACController:
    def __init__(self, id, name=None, loc=None, status=-1, ip='0.0.0.0', port='1234'):
        self.type = 'ac'
        self.id = id
        self.name = name
        self.location = loc
        self.status = status
        self.ip = ip
        self.port = port

    def turn_on(self):
        self.status = 0

    def turn_off(self):
        self.status = -1


class TempSensor:
    def __init__(self, id, desc, name=None, loc=None, temp=31, ip='0.0.0.0', port='1234'):
        self.type = 'TEMP'
        self.id = id
        self.name = name
        self.location = loc
        self.data = temp
        self.ip = ip
        self.port = port
        self.controller = -1
        self.low = 15
        self.high = 35
        self.placeholder = desc

    def temp_up(self):
        if self.data < self.high:
            inc = round(random.uniform(0, 1))
            self.data += inc

    def temp_down(self):
        if self.data > self.low:
            dec = round(random.uniform(1, 2))
            self.data -= dec

    def bind_controller(self, obj):
        self.controller = obj

    def genRandom(self):
        # value = self.data
        """if self.controller == -1:
            self.temp_up()
        else:
            self.temp_down()
        # return value
        return self.data, self.controller
        """
        self.data = random.randrange(self.low, self.high)
        return self.data, self.controller


class LuxSensor:
    def __init__(self, id, desc, name=None, loc=None, ip='0.0.0.0', port='1234'):
        self.type = 'LIGHT'
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.location = loc
        self.low = 0
        self.high = 20
        self.controller = -1
        self.data = 0
        self.placeholder = desc

    def genRandom(self):
        self.data = random.randrange(self.low, self.high) if self.controller == -1 else 20
        return self.data, self.controller


list_of_people = list(range(100000))
list_of_people_boarded = []
sleep_timers = [0, 0]


class BiometricSensor:
    def __init__(self,  id, desc, name=None, loc=None, ip='0.0.0.0', port='1234'):
        self.type = 'BIOMETRIC'
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.location = loc
        self.controller = -1
        self.placeholder = desc
        ch = random.choice(list_of_people)
        while ch in list_of_people_boarded and len(list_of_people_boarded) < len(list_of_people):
            ch = random.choice(list_of_people)
        list_of_people_boarded.append(ch)
        self.data = [self.placeholder, ch]

    def genRandom(self):
        timer = random.choice(sleep_timers)
        time.sleep(timer)
        ch = random.choice(list_of_people)
        while ch in list_of_people_boarded and len(list_of_people_boarded)<len(list_of_people):
            ch = random.choice(list_of_people)
        list_of_people_boarded.append(ch)
        self.data = [self.placeholder, ch]
        return self.data, self.controller


iiit_loc = [30.44523, 40.54232]
barricades = [[20.34535, 41.34234], [18.42342, 35.45453], [
    24.42342, 56.45453], [27.42342, 60.45453], [10.42342, 21.45453]]
places = [[12.34535, 23.34234], [15.42342, 17.45453], [19.42342, 43.45453],
          [27.321, 60.314], [10.4346, 46.332], [33.4346, 32.332], [10.2, 19.332], [23.12, 49.55],
          [20.321, 61.314], [30.4346, 45.332], [9.4346, 32.332], [17.2, 25.332], [23.12, 35.55]]

gps_weights = [0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]


class GPSSensor:
    def __init__(self,  id, desc, name=None, loc=None, ip='0.0.0.0', port='1234'):
        self.type = 'GPS'
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.location = loc
        self.controller = -1
        self.placeholder = desc
        self.data = [self.placeholder, random.choice(places)]

    def genRandom(self):
        ch = random.choice(gps_weights)
        if ch == 0:
            self.data = [self.placeholder, iiit_loc]        
        elif ch == 1:
            self.data = [self.placeholder, random.choice(barricades)]
        else:
            self.data = [self.placeholder, random.choice(places)]

        return self.data, self.controller


class Oximeter:
    def __init__(self, id, desc, name=None, loc=None, ip='0.0.0.0', port='1234'):
        self.type = 'OXIMETER'
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.location = loc
        self.low = 85
        self.high = 96
        self.controller = -1
        self.data = 0
        self.placeholder = desc

    def genRandom(self):
        self.data = random.randrange(self.low, self.high)
        return self.data, self.controller
