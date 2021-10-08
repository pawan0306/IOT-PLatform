import time

SENSOR_TYPES = {'temp': -1}


registry = open('sensor_registry.txt', 'r')
while True:

    sensors = registry.readlines()
    print("Sesnors", sensors,'\n')
    if len(sensors) > 0:
        for sensor in sensors:
            print(sensor.strip('\n'))
            sinfo, nwinfo = sensor.split(':')
            stype = sinfo.split('_')[0]
            ip, port = nwinfo.split('_')
            SENSOR_TYPES[stype] += 1
            topic = stype + "_" + str(SENSOR_TYPES[stype])

            print(sinfo + ":" + nwinfo + ":" + topic)

    time.sleep(10)