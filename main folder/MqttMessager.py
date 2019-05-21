import paho.mqtt.client as paho
import logging

    ##MQTT
    #broker = "192.168.1.18" #ip do servidor local padrao estatico
    #port = 1883 # padrao

class MqttMessager:
    
    def __init__(self, broker, port):
        self.cl = paho.Client("control1")
        self.cl.connect(broker, port)
        ##LOG
        LOG_FILE =  "../Logs/mqtt_log.log"
        logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

    def on_publish(self, client, userdata, result): #callback
        logging.debug("ip:" + self.broker + ":" + str(self.port) + ";published: "+ self.topic + ":" + self.message) ##log
        pass

    def publishMessage(self, topic, message):
        #cl = paho.Client("control1")
        #cl.connect(broker, port)    
        self.cl.on_publish = self.on_publish
        ret = self.cl.publish(topic, message)    
        return ret