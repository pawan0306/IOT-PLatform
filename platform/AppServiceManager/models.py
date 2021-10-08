#!/usr/bin/env python3


class Application:
    def __init__(self, app_id, user_id, sensor_list, ip, port, ram_req, cpu_req, app_path, algo_path):
        self.app_id = app_id
        self.user_id = user_id
        self.sensor_list = sensor_list
        self.ip = ip
        self.port = port
        self.ram_req = ram_req
        self.cpu_req = cpu_req
        self.app_path = app_path
        self.algo_path = algo_path


class Server:
    def __init__(self, id, ip, port, active, health, num_apps, username, password):
        self.id = id
        self.ip = ip
        self.port = port
        self.active = active
        self.health = health
        self.num_apps = num_apps
        self.username = username
        self.password = password


KAFKA_TOPIC_SERVER_LIST = 'server_list'
KAFKA_TOPIC_NODE_SERVER_ASSIGN_LIST = 'node-server-assign'
KAFKA_TOPIC_LOGGER = 'logger-listen'
