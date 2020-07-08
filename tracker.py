import json
import cellular
import machine
import socket
import gps
import utime

#todo adc for battery
#todo gps - try glonass, other settings
#todo accel

SETTINGS = {
              'apn': "internet.beeline.ru", 
              'login': "beeline",
              'password': "beeline",
              'send_sms_on_call': True,
              'sms_template': "http://www.google.com/maps/place/{lat},{lng}",
              'rtt_server': "5.9.136.109",
              'rtt_port': 3359,
           }

gps_state = False;
gprs_state = False

def set_gprs_state(state):
    global gprs_state

    prev_state = gprs_state;

    if state and not gprs_state:
        cellular.gprs(SETTINGS['apn'], SETTINGS['login'], SETTINGS['password'])
    else:
        if not state and gprs_state :
             cellular.gprs(False)

    gprs_state=state;
    return prev_state

def set_gps_state(state):
    global gps_state

    prev_state = gps_state;

    if state and (not gps_state) :
        gps.on()
    else:
        if not state and gps_state :
            gps.off()

    gps_state=state;
    return prev_state


def get_coordinates():
    global gps_state

    if gps_state :
        return gps.get_location();

    #todo agps

    return (0,0)

def on_call_handler(number):
    cellular.on_call(on_call_handler)

    if isinstance(number, str) :
        cellular.dial(False)

        if not SETTINGS['send_sms_on_call']:
            return

        prev_state = set_gps_state(True)

        coords = get_coordinates()

        text = SETTINGS['sms_template'].format(lat=coords[0], lng=coords[1])
        cellular.SMS('+' + number, text).send()

        set_gps_state(prev_state)

def get_rtt_string():
    coords = get_coordinates()
    tm = utime.localtime();

    return "rtt003," + \
            str(cellular.get_imei()) + "," + \
            str(coords[0]) + "," + \
            str(coords[1]) + "," + \
            "00," + \
            "00," + \
            "000," + \
            "{:03d},".format(machine.get_input_voltage()[1]) + \
            "{:4d}{:02d}{:02d},".format(tm[0], tm[1], tm[2]) + \
            "{:02d}{:02d}{:02d},".format(tm[3], tm[4], tm[5]) + \
            "000," + \
            "{:02d},".format(gps.get_satellites()[1]) + \
            "{:02d},".format(cellular.get_signal_quality()[0]) + \
            "A," + \
            "0\r\n"

def send_rtt_coordinates():
    s = socket.socket()
    try:
        s.connect((SETTINGS['rtt_server'], SETTINGS['rtt_port']))
        print(get_rtt_string())
        s.write(get_rtt_string())
    finally:
        s.close()


def main_loop():
    set_gps_state(True)

    while(True):
        try: 
            set_gprs_state(True)
            send_rtt_coordinates()
        except Exception as err:
            print("OS error: {0}".format(err));
            cellular.SMS('+79169542241', "OS error: {0}".format(err)).send()
            set_gprs_state(False)

#        machine.set_idle(True)
        utime.sleep(60)
#        machine.set_idle(False)

cellular.on_call(on_call_handler)

main_loop()

