#http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
import paho.mqtt.client as paho

broker = "192.168.1.18"
port = 1883
def on_publish(client, userdata, result): #callback
    print("data published \n")
    pass

client1 = paho.Client("control1")
client1.on_publish = on_publish
client1.connect(broker, port) #Estabelecer conexão
ret = client1.publish("maincore/teste","FOI MESMO EU QUE NAO VI O ÇEDILHA") #publish TOPIC + MESSAGE  