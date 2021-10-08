#!/usr/bin/env python3

import os
from flask import Flask, render_template, request, jsonify
import validate_instance
import sensor_manager as sm
import json


PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
registry_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensor_registry.txt")
repository_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensor_repository.json")
app = Flask("Sensor Services", template_folder=os.path.join(PARENT_DIR, 'templates'))


@app.route("/new-sensor", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        #global SENSOR_TYPES
        stype = data.get('type')

        #print(stype)
        #if stype not in SENSOR_TYPES:
        #    print("Adding new sensor...")
        #    SENSOR_TYPES[stype] = -1

        sid = data.get('id')
        name = data.get('name')
        output = str(data.get('output'))
        # with open(repository_path, 'a') as f:
        #     line = '_'.join([sid, name, output])
        #     line = stype + ":" + line
        #     print(line)
        #     f.write(line + '\n')
        return render_template("success.html",message="success")

    return render_template("new_sensor.html", message="success")


@app.route("/install-sensor", methods=["GET", "POST"])
def install():
    if request.method == "POST":
        data = request.form
        stype = data.get('type')
        if validate_instance.validate_instance(stype):
            loc = data.get('location')
            ip = data.get('ip')
            port = data.get('port')
            desc = str(data.get('desc'))

            with open(registry_path, 'a') as f:
                line = stype + ":" + desc + "_" + loc + ":" + ip + "_" + port
                f.write(line + '\n')
            return render_template("success.html",message="success")
        else:
            return render_template("invalid.html", message="success")
    return render_template("install_sensor.html", message="success")


@app.route("/get-data", methods=["POST"])
def getdata():
    payload = request.get_json()
    topic_list = payload['sensor']
    data = []
    for topic in topic_list:
        d = sm.get_data(topic)
        data.append(d)

    payload = {"data": data}
    response = app.response_class(
        response=json.dumps(payload),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/set-data", methods=["POST"])
def setdata():
    payload = request.get_json()
    controllers = payload['controller']
    topic_list = list(controllers.keys())
    # data = []
    for topic in topic_list:
        msg = {"topic":topic, "value":controllers[topic]}
        sm.set_data(msg)

    response = app.response_class(
        response=json.dumps({'data': 1}),
        status=200,
        mimetype='application/json'
    )
    return response


def init_services():
    app.run(port=5050, debug=True)


if __name__ == "__main__":
    init_services()
    