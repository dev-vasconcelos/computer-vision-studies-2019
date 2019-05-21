import paho.mqtt.client as paho
import logging

    ##MQTT
broker = "192.168.15.157" #ip do servidor local padrao estatico
port = 1883 # padrao
topic = "maincore/smart"
message = "{'recognized':'1','name':'Pedro ivo','pleaseable':'True'}"

cl = paho.Client("control1")
cl.connect(broker, port)
cl.publish(topic, message);
