import json
import cellular
import machine
import socket
import select
import gps
import utime
import time

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
              'min_bat_adc': 665,
              'bat_adc_scale': 95,
           }

gps_state = False;
gprs_state = False
st = time.time()
adc0 = machine.ADC(0)
led = machine.Pin(27, machine.Pin.OUT, 0)

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
        last_call='+' + number


def send_coords_by_sms(number):
    if not SETTINGS['send_sms_on_call']:
        return

    try:
        prev_state = set_gps_state(True)

        coords = get_coordinates()

        text = SETTINGS['sms_template'].format(lat=coords[0], lng=coords[1])
        cellular.SMS(number, text).send()
    finally:
        set_gps_state(prev_state)

def get_battery():
    return int((min(adc0.read(), 760) - SETTINGS['min_bat_adc'])/SETTINGS['bat_adc_scale'] * 1000);

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
            "{:03d},".format(get_battery()) + \
            "{:4d}{:02d}{:02d},".format(tm[0], tm[1], tm[2]) + \
            "{:02d}{:02d}{:02d},".format(tm[3], tm[4], tm[5]) + \
            "000," + \
            "{:02d},".format(gps.get_satellites()[1]) + \
            "{:02d},".format(cellular.get_signal_quality()[0]) + \
            "A," + \
            "0\r\n"

def connect_with_timeout(s, server, port, timeout):
    s.setblocking(0);

    try:
        s.connect((server, port))
    except Exception as err:
        pass

    readable,writable,exceptionavailable = select.select([s],[s],[s],timeout)
    
    for s in writable:
        s.setblocking(1)
        return s

    raise Exception("Connect timeout")

def send_rtt_coordinates():
    s = socket.socket()
    s.settimeout(10.0)
    try:
        connect_with_timeout(s, SETTINGS['rtt_server'], SETTINGS['rtt_port'], 5)
        print(get_rtt_string())
        s.write(get_rtt_string())
    finally:
        s.close()


def main_loop():
    global led
    set_gps_state(True)
    machine.watchdog_on(120)

    while(True):
        led.value(1)
        print((time.time()-st))
        machine.watchdog_reset()
        try: 
            set_gprs_state(True)
            send_rtt_coordinates()
        except Exception as err:
            print("OS error: {0}".format(err));
            set_gprs_state(False)

        led.value(0)
        machine.set_idle(True)
        utime.sleep(10)
        machine.set_idle(False)

cellular.on_call(on_call_handler)

machine.set_min_freq(machine.PM_SYS_FREQ_13M)

main_loop()

