##MQTT USAGE OWN
import MqttMessager as mqttmessi

messi = mqttmessi.MqttMessager("192.168.1.18", 1883)

messi.publishMessage("maincore/teste", "mensagem vinda de outro file")
##MQTT USAGE OWN