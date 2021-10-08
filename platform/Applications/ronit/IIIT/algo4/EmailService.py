import API
import time

api = API.sensorapi()
api.display(f'{time.ctime()} :: Bus Found near the barricade')
api.sendMail(f'{time.ctime()} :: Bus Found near the barricade') 