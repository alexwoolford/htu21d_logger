#!/usr/bin/env python

from sense_hat import SenseHat
import time
import socket
from kafka import KafkaProducer
import json
import cronus.beat as beat


class SensorHatLogger:

    """
    Logs the hostname, time (unixtime), temperature, humidity, and pressure to Kafka in JSON format. The data is
    generated by a Raspberry Pi with a Sense Hat: https://www.raspberrypi.org/products/sense-hat/
    
    This captures a read approx. every 10 seconds.

    TODO: https://github.com/initialstate/wunderground-sensehat/wiki/Part-3.-Sense-HAT-Temperature-Correction
    
    """

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='hdp01.woolford.io:6667')
        self.sense = SenseHat()
        self.sensor_record = dict()

    def read_values_from_sensor(self):
        self.sensor_record['host'] = socket.gethostname()
        self.sensor_record['timestamp'] = int(time.time())
        self.sensor_record['temperature'] = self.sense.get_temperature()
        self.sensor_record['humidity'] = self.sense.get_humidity()
        self.sensor_record['pressure'] = self.sense.get_pressure()

    def send_record_to_kafka(self):
        sensor_record_json = json.dumps(self.sensor_record)
        self.producer.send("temperature_humidity_json", sensor_record_json)

    def run(self):
        self.read_values_from_sensor()
        self.send_record_to_kafka()


if __name__ == "__main__":
    sensor_hat_logger = SensorHatLogger()
    beat.set_rate(0.1)
    while beat.true():
        sensor_hat_logger.run()
        beat.sleep()