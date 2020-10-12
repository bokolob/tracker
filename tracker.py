import json
import cellular
import machine
import socket
import select
import gps
import utime
import time

import urequests
import gprs
import location
import lis3dsh
import softi2c

from settings import get_property,set_property
from commands import run_cmd, check_admin_number

#todo adc for battery
#todo agps
#todo accel
#Обновлять конфигурацию через СМС
#В долгом сне отключать gps
#Конфигурация через СМС
#Режимы работы - обновлениея раз в 15 минут, раз в минуту, при движении
#Возможность использовать любую симкарту, любого оператора с любым тарифом. Трекер с жёсткой привязкой к производителю не нужен.
#Автономная работа в активном режиме не меньше суток
#Возможность переходить в спящий режим (по заряду батарейки, по команде etc). Выход из него — по звонку, по принятию SMS, etc.
#Открытый формат данных и возможность задавать куда эти данные отправлять
#В родном приложении — выбор поставщика карт
#Там же: показ не только положение трекера, но и приёмника. Это очень важно при отсутствии рядом видимых ориентиров, например, за пределами города.
#

adc0 = machine.ADC(0)
led = machine.Pin(27, machine.Pin.OUT, 0)
stat=machine.Pin(17,machine.Pin.IN,1)
network_status = -1
si = softi2c.SoftI2C()
lis = lis3dsh.main()

sms_requested = None
interrupt = False

def sms_handler(sms):
    cellular.on_new_sms(sms_handler)
    msg=sms.message

    if usb_connected():
        s.writeRegister("sms effect")

    print("sms_handler")
    result = run_cmd(sms.phone_number, [ word.lower() for word in msg.split() ])

    remove_all_sms()
    if result is not None:
        cellular.SMS(sms.phone_number, result).send(0)
    

def network_handler(status):
    global network_status

    if network_status != status:
        print("network status: "+ str(status))
        network_status = status
        interrupt=True

    cellular.on_status_event(network_handler)


def on_call_handler(number):
    global sms_requested
    cellular.on_call(on_call_handler)

    if isinstance(number, str):
        cellular.dial(False)

        phone = '+' + number
        if check_admin_number(phone) and get_property('send_sms_on_call'):
            interrupt=True
            sms_requested = phone


def send_coords_by_sms(number):
    try:
        print("Sending coords")
        coords = location.get_coordinates()
        text = get_property('sms_template').format(lat=coords[0], lng=coords[1])
        print("Sending "+text)
        cellular.SMS(number, text).send(0)
    except Exception as err:
        pass


def get_battery():
    value =  adc0.read();
    v = max( get_property('min_bat_adc'), value)
    v = min( get_property('max_bat_adc'), v)
    return (v-get_property('min_bat_adc'))/( get_property('max_bat_adc')-get_property('min_bat_adc')) * 100;


def get_rtt_string(coords):
    tm = utime.localtime();
    source = 'A' if coords[2] else 'V'

    return "rtt003," + \
            str(cellular.get_imei()) + "," + \
            str(coords[0]) + "," + \
            str(coords[1]) + "," + \
            "00," + \
            "00," + \
            "000," + \
            "{:03.0f},".format(get_battery()) + \
            "{:4d}{:02d}{:02d},".format(tm[0], tm[1], tm[2]) + \
            "{:02d}{:02d}{:02d},".format(tm[3], tm[4], tm[5]) + \
            "000," + \
            "{:02d},".format(gps.get_satellites()[1]) + \
            "{:02d},".format(cellular.get_signal_quality()[0]) + \
            source + "," + \
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
        coords = location.get_coordinates()
        print(get_rtt_string(coords))
        connect_with_timeout(s, get_property('rtt_server'), get_property('rtt_port'), 10)
        s.write(get_rtt_string(coords))
    finally:
        s.close()

def delay(ms):
    global interrupt
    f=open("t/gps.log","a")
    machine.set_idle(True)

    step = 1000
    prev_gps_state = location.gps_state

    if ms > 5 * 60 * 1000:
        location.set_gps_state(False)

    while ms > 0:
        if interrupt:
            interrupt = False
            f.close()
            raise OSError(4) #EINTR

        if ms < step:
            step = ms

        rec=gps.nmea_data()[0]
        coords = gps.get_location()
        if rec[1]:
            f.write(str(rec)+" "+str(coords)+"\n")

        utime.sleep_ms(step)
        ms -= step
        machine.watchdog_reset()

    location.set_gps_state(prev_gps_state)
    machine.set_idle(False)
    f.close()


def main_iteration():
    global led
    global sms_requested

    led.value(1)
    machine.watchdog_reset()

    try:
        if sms_requested is not None:
            send_coords_by_sms(sms_requested)
            sms_requested = None

        gprs.wait_gprs()
        machine.set_min_freq(machine.PM_SYS_FREQ_39M)
        send_rtt_coordinates()
    except Exception as err:
        print("OS error: {0}".format(err));
        try:
            admins = get_property("admin_numbers")

            if len(admins) > 0:
                cellular.SMS(admins[0], "OS error: {0}".format(err)).send(0)

        except Exception as e:
            pass
    finally:
        machine.watchdog_reset()
        led.value(0)


def main_loop():
    while (True):

        if charging():
            s.writeRegister("charging effect")
        else:
            si.writeRegister("stop_charging_effect")

        remove_all_sms()
        main_iteration()
        delay(get_property('track_delay_minutes') * 60 * 1000)

        if deep_sleep_allowed and no_move_for_a_long_time():
            send_sms()

            if usb_connected():
                s.writeRegister("sleep effect")
            
            si.writeRegister("deep_sleep")

        if is_nth_iteration:
            si.writeRegister("ping_effect")

def start():
    print("GPS tracking software")
    
    power_on_reason = si.readRegister(0x8, 3)
    lis.set_wake_up()

    if power_on_reason == "sleep_timeout":
        check_for_sms()
        if deep_sleep_allowed:
            si.writeRegister("deep_sleep")
    else:
        if usb_connected():
            s.writeRegister("wake_up effect")

    location.set_gps_state(True)
    
    callbacks = gprs.Callbacks()
    callbacks.sms_handler = sms_handler;
    callbacks.call_handler = on_call_handler;
    callbacks.network_handler = network_handler
    
    gprs.set_callbacks(callbacks)
    gprs.init()

    machine.watchdog_on(120)
    machine.set_min_freq(machine.PM_SYS_FREQ_39M)

    main_loop()

