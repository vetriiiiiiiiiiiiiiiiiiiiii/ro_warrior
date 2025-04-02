import paho.mqtt.client as mqtt

class Communication:
    def __init__(self, broker, port):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()

    def connect(self):
        """Connects to the MQTT broker"""
        try:
            self.client.connect(self.broker, self.port)
            self.client.loop_start()
        except Exception as e:
            print(f"Error connecting to MQTT: {e}")

    def publish_data(self, topic, message):
        """Publishes data to MQTT topic"""
        self.client.publish(topic, message)