import os
import json
import time
import paho.mqtt.client as mqtt
import telebot

bot_token = os.environ["EXCHANGE_BOT_TOKEN"]
bot = telebot.TeleBot(bot_token)

topic_sub_state = 'customer_detector/exchanges/customer_detector_0001/state'
topic_sub_events = 'customer_detector/exchanges/customer_detector_0001/events'
topic_pub_ctl = 'customer_detector/exchanges/customer_detector_0001/ctl'

mqtt_host = 'korotach.com'
mqtt_user = 'igor'
mqtt_password = 'igor1315'
debug = True
state_filename = "./states/" + str(time.strftime("%Y%m%d")) + "_state_.csv"
events_filename = "./events/" + str(time.strftime("%Y%m%d")) + "_events_.csv"
heart_beat_time = time.time()
event_time = heart_beat_time
heart_is_beating = False
max_heart_interval = 23  # max heart beat interval in sec.


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
    global heart_beat_time
    global event_time
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
            # print("I'm here -- ", state_filename)
            state_file = open(state_filename, 'a')
            state_file.write(str(time.strftime("%d.%m.%Y %H:%M:%S")) +
                             ', ' + str(d['status']) +
                             ', ' + str(d['customer']) +
                             ', ' + str(d['duration']) +
                             ', ' + str(d['obstacles']) + '\n')
            state_file.close()
            heart_beat_time = time.time()
        if 'event' in d.keys():
            event_time = time.time()
            events_file = open(events_filename, 'a')
            events_file.write(str(time.strftime("%d.%m.%Y %H:%M:%S")) +
                              ', ' + str(d['event']) +
                              ', ' + str(d['duration']) + '\n')
            events_file.close()


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
    state_filename = "./states/" + str(time.strftime("%Y%m%d")) + "_state_.csv"
    events_filename = "./events/" + str(time.strftime("%Y%m%d")) + "_events_.csv"
    now = time.time()
    heart_interval = now - heart_beat_time
    print('heart_interval is: ', heart_interval)
    if heart_interval >= max_heart_interval and heart_is_beating:
        warning_msg = 'heart of exchange stopped for more than ' + str(max_heart_interval) + ' sec.'
        bot.send_message(-1001440639497, warning_msg)
        event_duration = now - event_time
        event_time = now
        warning_file = open(events_filename, 'a')
        warning_file.write(str(time.strftime("%d.%m.%Y %H:%M:%S")) +
                           ', ' + warning_msg +
                           ', ' + str(int(heart_interval*1000)) + '\n')
        warning_file.close()
        heart_is_beating = False
    else:
        if not heart_is_beating and heart_interval < max_heart_interval:
            warning_msg = 'heart of exchange started to beat'
            bot.send_message(-1001440639497, warning_msg)
            event_duration = now - event_time
            event_time = now
            print('writing to a file: ', events_filename, ' msg: ', warning_msg)
            warning_file = open(events_filename, 'a')
            warning_file.write(str(time.strftime("%d.%m.%Y %H:%M:%S")) +
                               ', ' + warning_msg +
                               ', ' + str(int(event_duration*1000)) + '\n')
            warning_file.close()
            heart_is_beating = True
