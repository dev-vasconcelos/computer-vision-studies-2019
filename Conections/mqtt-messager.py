import paho.mqtt.client as paho
import logging

##LOG
LOG_FILE =  "../Logs/mqtt_log.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

##MQTT
broker = "192.168.1.18" #ip do servidor local padrao estatico
port = 1883 # padrao

def on_publish(client, userdata, result): #callback
    logging.debug("ip:" + broker + ":" + str(port) + ";published: "+ topic + ":" + message) ##log
    pass

def publishMessage(topic, message):
    cl = paho.Client("control1")
    cl.on_publish = on_publish
    cl.connect(broker, port)    

    ret = cl.publish(topic, message)    
    
    return ret