#!/usr/bin/env python3

from flask import *  # Flask,render_template,url_for,request,redirect
import pymongo as pm
from pymongo import *
from pprint import pprint
import json
import os
import zipParsing
from zipfile import ZipFile
import csv
import json
import threading
from _thread import *
import time
import sys
import shutil
from distutils.dir_util import copy_tree



sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm


curpath = str(os.path.dirname(os.path.realpath(__file__)))
# create repository directory if not present
reposPath = "../Applications"
if not os.path.exists(reposPath):
	os.mkdir(reposPath)

client = MongoClient("mongodb+srv://admin:admin123@cluster0.ze4na.mongodb.net")
db = client['IOT']
userTable = db['user_details']

# read credentials into set
userCredSet = set()
if os.path.isfile("platformUserCreds.txt"):
	with open("platformUserCreds.txt", "r") as file:
		for line in file:
			lst = line.strip().split(",")
			if len(lst) < 4:
				break
			tup = tuple([lst[0], lst[2], lst[3]])
			userCredSet.add(tup)

schedule_json_lst = ["start_time", "end_time","request_type",
					 "priority", "days", "interval", "duration"]
other_feilds_lst = ["userID", "appID", "algoID", "location", "placeholder","devID", "sensorList"]

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
'''@app.route('/')
def index():
	return render_template("signup.html")'''


def registerUser(instance):
	with open('platformUserCreds.txt', mode='a+') as file:
		line = ""
		for key in instance:
			line += instance[key] + ","
		lst = line[:-1].split(",")
		tup = tuple([lst[0], lst[2], lst[3]])
		userCredSet.add(tup)
		file.write(line[:-1]+"\n")


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
	get_flashed_messages()
	if request.method == "POST":
		data = request.form
		data = dict(data)
		x = userTable.find_one({"_id": data['username']})
		if x is not None:
			pprint(x)
			flash('User name already exists')
			return redirect(request.path)  # (url_for('sign_up'))
		mydict = {'_id': data['username'], 'email': data['email'],
				  'type': data['type'], 'password': data['pwd']}
		x = userTable.insert_one(mydict)
		print(data)
		# keys of dict are username, email,pwd
		# registerUser(data)
		# redirect to login
		flash('User name successfully registered')
		return redirect("/login")
	return render_template("sign_up.html")


def validateUser(instance):
	line = ""
	for key in instance:
		line += instance[key] + ","
	lst = line[:-1].split(",")
	tup = tuple([lst[0], lst[2], lst[1]])
	if tup in userCredSet:
		return True
	else:
		return False


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		#print("Got login request")
		data = request.form
		data = dict(data)
		print(data)
		x = userTable.find_one({"_id": data['user_id']})#, "password": data['pwd']})
		# valid = validateUser(req)
		if x is not None:
			pprint(x)
			if x['password'] != data['pwd']:
				flash('Incorrect password')
				return redirect(request.path)
			if x['type'].lower() == data['dname'].lower() and data['dname'].lower() == 'developer':
				# if req["dname"]=="Developer":
				return redirect(url_for('upload', usrname=data["user_id"]))
			elif x['type'].lower() == data['dname'].lower() and data['dname'].lower() == 'user':
				return redirect(url_for('action', usrname=data["user_id"]))
			else:
				flash('Invalid user type')
				return redirect(request.path) 
		else:
			flash('User name not found. Please register')
			return redirect(request.path)  # redirect("/login")

	return render_template("login.html")


def storeInRepo(username, zipPath):
	userRepoPath = reposPath + "/"+username
	if not os.path.exists(userRepoPath):
		os.mkdir(userRepoPath)
	with ZipFile(zipPath, 'r') as zipObj:
		zipObj.extractall(userRepoPath)
	os.remove(zipPath)


@app.route("/<usrname>/action",methods=["GET","POST"])
def action(usrname):
    if request.method=="POST":
        data=request.form
        req = dict(data)
        if req['action'] == 'dashboard':
            return redirect(url_for('dashboard',usrname=usrname))
        else:
            return redirect('/fill-form')

    return render_template("action.html",usrname=usrname)

@app.route("/<usrname>/dashboard",methods=["GET","POST"])
def dashboard(usrname):
    if request.method=="POST":
        data=request.form
        req = dict(data)
        #with open("user_details.json") as f:
        #    details = json.load(f.read())

        #if usrname in details.keys() and req["appID"] in details[usrname].keys() and req["algoID"] in details[usrname]["appID"]:
        if req['placeholder'] != '':
        	outputfile = req['placeholder']+'_'+usrname+'_'+req["appID"]+'_'+req["algoID"]
        else:
        	outputfile = req['location']+'_'+usrname+'_'+req["appID"]+'_'+req["algoID"]
        return render_template('monitor.html', filename=outputfile)
        #else:
        #    return "No such Application or Algorithm is registered"        

    return render_template("dashboard.html",usrname=usrname)


@app.route("/<filename>/monitor",methods=["GET","POST"])
def monitor(filename):
    if request.method=="GET":
        
        with open("../Data/"+filename, 'r') as f:
            return '<br>'.join(f.read().split('\n'))

        """with open('readline','w+') as r:
        	line = r.read()
        	print(line)
        	with open('../Data/'+filename,'r') as f:
        		data = f.read()
        		l = data.split('\n')
        		if len(l) > int(line):
        			line = len(l)+1
        			r.write(line)	
        			return l[line]+'<br>'

		"""

    if request.method=="POST":
        data=request.form
        req = dict(data)
        print(req)
        if req["action"] == "back":
            pass
        if req["action"] == "stop":
        	msg={}
        	msg['jid']=filename.split('/')[-1]
        	msg['action']='stop'
        	cm.send_message("AS", msg)
        	usr = filename.split('_')[1]
        	return redirect(url_for('dashboard',usrname=usr))

    return render_template("monitor.html",filename=filename)



# uploading the developer file to a directory
@app.route("/<usrname>/upload", methods=["GET", "POST"])
def upload(usrname):
	if request.method == "POST":

		file = request.files['file']
		if not os.path.exists(curpath+"/temp_zips"):
			os.mkdir(curpath+"/temp_zips")
		file.save(os.path.join(curpath+"/temp_zips", file.filename))
		zip_path = os.path.join(curpath+"/temp_zips", file.filename)
		valid = zipParsing.processZip(zip_path)
		if valid:
			storeInRepo(usrname, zip_path)
			return "Application is successfully deployed!"
		# upload to directory structure i.e mongo db in our case
		else:
			return "Errorrrrr!"

	return render_template("upload.html", username=usrname)


def get_schedule_dict(dict1):
	dict = {}
	for entry in schedule_json_lst:
		dict[entry] = dict1[entry]
	return dict


def get_dict(dict1):
	dict = {}
	dict["schedule"] = get_schedule_dict(dict1)
	for entry in other_feilds_lst:
		if entry == "sensorList":
			dict[entry] = dict1[entry].split(",")
			continue
		dict[entry] = dict1[entry]
	configPath = reposPath + "/" + \
		dict["devID"] + "/" + dict["appID"] + \
		"/" + dict["algoID"] + "/config.json"

	with open(configPath, "r") as file:
		x = json.load(file)
		dict["RAM"] = x["RAM"]
		dict["CPU"] = x["CPU"]
	return dict


@app.route("/fill-form", methods=["GET", "POST"])
def fill_form():
	if request.method == "POST":
		data = request.form
		req = dict(data)
		#print(req)
		msg = get_dict(req)
		msg["action"] = 'start'
		#print(msg)

		if msg['placeholder'] != '':
			newdir = msg['placeholder']+'_'+msg['userID']+'_'+msg["appID"]+'_'+msg["algoID"]
		else:
			newdir = msg['location']+'_'+msg['userID']+'_'+msg["appID"]+'_'+msg["algoID"]

		src = '../Applications/'+msg['devID']+'/'+msg['appID']+'/'+msg['algoID']
		dst = '../RunningApps/'+newdir
		if not os.path.exists(dst):
			os.mkdir(dst)
			copy_tree(src, dst)

		cm.send_message("AS", msg)

		return "Request Submitted"

	return render_template("service_request_form.html")


def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()


@app.route('/shutdown', methods=['GET'])
def shutdown():
	shutdown_server()
	return 'Server shutting down...'


app.run(debug=True)
