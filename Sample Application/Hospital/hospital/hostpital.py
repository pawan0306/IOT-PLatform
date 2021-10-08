import API

api = API.sensorapi()

while True:
    
    oxy = api.getData("OXYMETER")["data"] #{data:[[placeholderID, [x, y]]}
    for i in oxy:
        if i[1] < 80:
            api.display(f'{time.ctime()} :: {i[0]}:Low Oxygen level({i[1]}) detected! ')
            