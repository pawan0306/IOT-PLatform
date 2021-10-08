# Hackathon 2

## Launch services in SEPARATE TERMINALS

`zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties`

`kafka-server-start /usr/local/etc/kafka/server.properties`

`kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic server_list`

`kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic node-server-assign`

## Basic run instructions for deployer

- Run `node_manager.py` in one terminal
- Run `deployer.py`
