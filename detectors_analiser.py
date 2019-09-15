import os
import json
import time
import paho.mqtt.client as mqtt

topic_sub_state = 'customer_detector/exchanges/customer_detector_0001/state'
topic_sub_events = 'customer_detector/exchanges/customer_detector_0001/events'
topic_pub_ctl = 'customer_detector/exchanges/customer_detector_0001/ctl'

mqtt_host = 'korotach.com'
mqtt_user = 'igor'
mqtt_password = 'igor1315'
debug = True


def on_connect(mosq, obj, flags, rc):
    mqttc.subscribe(topic_sub_state, 0)
    mqttc.subscribe(topic_sub_events, 0)
    print("rc: " + str(rc))


def on_message(mosq, obj, msg):
    """
    get the state and events strings from device
    state string:
    {"status": "Ready", "customer": "left", "duration": 11123, "obstacles": 78}
    events string:
    {"event": "Customer arraived", "duration": 11125}
    """
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    json_string = ''
    d = {}
    try:
        json_string = msg.payload.decode('utf8')
    except UnicodeDecodeError:
        print("it was not a utf8-encoded unicode string")
    if json_string != '' and is_json(json_string):
        d = json.loads(json_string)
        if 'status' in d.keys():
            if d['status'].find('Ready') != -1:
                state = 'we successfully have gave goods out'


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mosq, obj, level, string):
    print(string)


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True


mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# mqttc.on_log = on_log
mqttc.username_pw_set(mqtt_user, password=mqtt_password)
# Connect
mqttc.connect(mqtt_host, 1883, 60)
# Continue the network loop
# mqttc.loop_forever()
mqttc.loop_start()
time.sleep(1)

while True:
    pass  # write the analityc's report
    time.sleep(1)
