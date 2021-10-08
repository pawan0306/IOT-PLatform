#!/usr/bin/env bash

# trap "exit" INT TERM ERR
# trap "kill 0" EXIT

#Initiating Kafka server

cd ~/kafka/bin/
gnome-terminal --window -- ./zookeeper-server-start.sh ~/kafka/config/zookeeper.properties
sleep 5
gnome-terminal --window -- ./kafka-server-start.sh ~/kafka/config/server.properties
sleep 7

cd -
cd platform/AppManager
pwd
gnome-terminal --window -- ./appManager.py
cd ..

cd AppServiceManager
pwd
gnome-terminal --window -- ./node_manager.py
gnome-terminal --window -- ./appService.py
gnome-terminal --window -- ./logger.py
cd ..

cd scheduler
pwd
gnome-terminal --window -- ./scheduler.py
cd ..

cd SensorManager
pwd
gnome-terminal --window -- ./sensor_services.py
gnome-terminal --window -- ./init.py


#Registering Kafka topics
#  .~/kafka/bin/./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic AS &
#  .~/kafka/bin/./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic DS &
#  .~/kafka/bin/./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic SM_to_Deployer_get &
#  .~/kafka/bin/./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic Deployer_to_SM_data &
#  .~/kafka/bin/./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic SM_to_Deployer_data &

# Initiating modules
# python3 ~/vscode/platform/Hackathon2_AppManager/appManager.py &

# python3 ~/vscode/platform/AppServerManager/node_manager.py &

# python3 ~/vscode/platform/AppServerManager/deployment.py&

# python3 ~/vscode/platform/SensorManager/init.py &

# python3 ~/vscode/platform/scheduler/scheduler.py





# # cd Service_Lifecycle
# sudo python3 platform/Service_Lifecycle/service_lifecycle.py &
# # cd ..


# # cd Server_Lifecycle
# sudo python3 platform/Server_Lifecycle/server_lifecycle.py &
# # cd ..


# # cd Deployment_Manager
# sudo python3 platform/Deployment_Manager/DeploymentManager.py &
# # cd ..


# # cd SensorManager
# sudo python3 platform/SensorManager/SensorManager.py &
# # cd ..

# # cd Action_Manager
# sudo python3 platform/Action_Manager/actionserver.py &
# # cd ..

# # cd Scheduler
# sudo python3 platform/Scheduler/sched.py &
# cd ..

# wait