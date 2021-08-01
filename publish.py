#!/usr/bin/python3
# this file contains the code to publish parsed messages to your system
# currently there is only MQTT implemented, which can be configured in the central config

import logging
import paho.mqtt.publish

#internal imports
import config

def process(msg):
    if config.mqtt_enabled:
        dateTime = msg["dateTime"]

        # multiple topics: topic, payload, qos, retain
        mqttMsg = [(config.mqtt_topic_prefix + "zaehlerstand_bezug", msg["A+"], config.mqtt_qos, config.mqtt_retain),
                   (config.mqtt_topic_prefix + "zaehlerstand_lieferung", msg["A-"], config.mqtt_qos, config.mqtt_retain),
                   (config.mqtt_topic_prefix + "leistung_bezug", msg["P+"], config.mqtt_qos, config.mqtt_retain),
                   (config.mqtt_topic_prefix + "leistung_lieferung", msg["P-"], config.mqtt_qos, config.mqtt_retain),
                   (config.mqtt_topic_prefix + "timestamp", f"{dateTime['year']}-{dateTime['day']}-{dateTime['month']} {dateTime['hour']}:{dateTime['minute']}:{dateTime['day']}", config.mqtt_qos, config.mqtt_retain),]

    logging.debug("publishing: " + "{0}".format(mqttMsg))
        
    try:
        paho.mqtt.publish.multiple(mqttMsg, hostname=config.mqtt_hostname, auth=config.mqtt_auth)
    except Exception as e:
        logging.error("error while publishing {0}".format(e))