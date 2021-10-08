from zipfile import ZipFile
import json
import os

sensor_types_supported = {}
controller_types_supported = {}

def validateSensorTypes(sensorList):
    global sensor_types_supported
    global controller_types_supported
    for sensor in sensorList:
        if sensor not in sensor_types_supported:
            print("Sensor types provided are not supported by platform")
            return False
    return True


def validateControllerTypes(controllerList):
    global sensor_types_supported
    global controller_types_supported
    for controller in controllerList:
        if controller not in controller_types_supported:
            print("Controller types provided are not supported by Platform")
            return False
    return True

def checkAlgosExist(configAlgoList,algosInApp):
    global sensor_types_supported
    global controller_types_supported


    configAlgoList.sort()
    algosInApp.sort()
    if configAlgoList == algosInApp:
        return True
    print("Algorithms Folders in config and zip are contradicting..")
    return False

def validateRootConfig(zipFileName,configPath,algoFoldersPath):
    global sensor_types_supported
    global controller_types_supported
    algosFound  = [item.split("/")[-2] for item in algoFoldersPath]
    archive = ZipFile(zipFileName, 'r')
    content = archive.read(configPath)
    data = json.loads(content)
    
    valid_flag = True
    valid_flag = valid_flag and validateSensorTypes(data["sensor_types"])
    valid_flag = valid_flag and validateControllerTypes(data["controller_types"])
    valid_flag = valid_flag and checkAlgosExist(data["Algorithms"],algosFound)

    return valid_flag


def checkPythonFilesExist(configFilesList,filesInAlgo):
    global sensor_types_supported
    global controller_types_supported
    configFilesList.sort()
    filesInAlgo.sort()
    print(configFilesList,filesInAlgo)
    if configFilesList == filesInAlgo:
        return True
    print("Files in algorithms and files in config of Algo are contradicting")
    return False

def validateAlgoConfig(zipFileName,configPath,pythonFilePaths):
    global sensor_types_supported
    global controller_types_supported


    filesFound  = [item.split("/")[-1] for item in pythonFilePaths if item.endswith(".py")]
    archive = ZipFile(zipFileName, 'r')
    content = archive.read(configPath)
    data = json.loads(content)
    
    valid_flag = True
    valid_flag = valid_flag and validateSensorTypes(data["sensor_types"])
    valid_flag = valid_flag and validateControllerTypes(data["controller_types"])
    valid_flag = valid_flag and checkPythonFilesExist(data["files"],filesFound)

    return valid_flag


def validateAlgoFolders(zipFileName,algoFoldersPath):
    global sensor_types_supported
    global controller_types_supported

    listOfiles = []
    with ZipFile(zipFileName, 'r') as zipObj:
        listOfiles = zipObj.namelist()
    archive = ZipFile(zipFileName, 'r')
    for algoFolder in algoFoldersPath:
        filesInAlgoFolder = [item for item in listOfiles if item.startswith(algoFolder)][1:]
        algoConfigPath = ""
        pythonFilesPath = []
        for item in filesInAlgoFolder:
            if item.endswith(".json"):
                algoConfigPath = item
            elif item.endswith(".py"):
                pythonFilesPath.append(item)
        if not validateAlgoConfig(zipFileName,algoConfigPath,filesInAlgoFolder):
            return False
    return True      
        
        
def initialize_variable():
    global sensor_types_supported
    global controller_types_supported
    #read supported sensor types
    with open('sensors_supported.txt', 'r') as file:
        lst = file.readlines()
        sensor_types_supported = set([item.strip() for item in lst])

    
    #read supported controller types
    with open('controllers_supported.txt', 'r') as file:
        lst = file.readlines()
        controller_types_supported = set([item.strip() for item in lst])




def processZip(zipFileName):
    initialize_variable()
    with ZipFile(zipFileName, 'r') as zipObj:
        listOfiles = zipObj.namelist()
        algoFoldersPath = []
        rootConfigPath = ""
        for item in listOfiles:
            if len(item.split("/")) == 2 and item.endswith(".json"):
                rootConfigPath = item
            elif item.endswith("/"):
                algoFoldersPath.append(item)
        algoFoldersPath = algoFoldersPath[1:]

        valid_flag = True
        valid_flag = valid_flag and validateRootConfig(zipFileName,rootConfigPath,algoFoldersPath)
        valid_flag = valid_flag and validateAlgoFolders(zipFileName,algoFoldersPath)

        if valid_flag:
            print("Application zip file is compatable with Platfrom.")
        
        return valid_flag


# sensor_types_supported = {}
# #read supported sensor types
# with open('sensors_supported.txt', 'r') as file:
#     lst = file.readlines()
#     sensor_types_supported = set([item.strip() for item in lst])

# controller_types_supported = {}
# #read supported controller types
# with open('controllers_supported.txt', 'r') as file:
#     lst = file.readlines()
#     controller_types_supported = set([item.strip() for item in lst])

# usr_pwd_dict = dict()
# # create dictionary with username and password
# with open('usr_pwd.txt', 'r') as file:
#     for line in file:
#         key, value = [item.strip() for item in line.split(":")]
#         usr_pwd_dict[key] = value

        
# processZip("App.zip")
