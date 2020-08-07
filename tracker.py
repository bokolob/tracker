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


SETTINGS = {
              'apn': "internet.beeline.ru", 
              'login': "beeline",
              'password': "beeline",
              'send_sms_on_call': True,
              'sms_template': "http://www.google.com/maps/place/{lat},{lng}",
              'rtt_server': "5.9.136.109",
              'rtt_port': 3359,
              'min_bat_adc': 678,
              'max_bat_adc': 751,
              'bat_adc_scale': 95,
              'track_delay_minutes': 1,
           }

NTW_REG_BIT =  0x01
NTW_ROAM_BIT = 0x02
NTW_REG_PROGRESS_BIT = 0x04
NTW_ATT_BIT =  0x08
NTW_ACT_BIT = 0x10

gps_state = False
st = time.time()
adc0 = machine.ADC(0)
led = machine.Pin(27, machine.Pin.OUT, 0)
led2 = machine.Pin(28, machine.Pin.OUT, 0)
stat=machine.Pin(17,machine.Pin.IN,1)

def network_handler(status):
    print("network status: "+ str(status))
    cellular.on_status_event(network_handler)


def set_gps_state(state):
    global gps_state

    prev_state = gps_state;

    if state and (not gps_state):
        gps.on()
    else:
        if not state and gps_state:
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

    if isinstance(number, str):
        cellular.dial(False)
        last_call='+' + number
        send_coords_by_sms(last_call)


def send_coords_by_sms(number):
    if not SETTINGS['send_sms_on_call']:
        return

    try:
        print("Sending coords")
        prev_state = set_gps_state(True)

        coords = get_coordinates()

        text = SETTINGS['sms_template'].format(lat=coords[0], lng=coords[1])
        print("Sending "+text)
        cellular.SMS(number, text).send()
    finally:
        machine.watchdog_reset()
        set_gps_state(prev_state)


def get_battery():
    value =  adc0.read();
    v = max( SETTINGS['min_bat_adc'], value)
    v = min( SETTINGS['max_bat_adc'], v)
    return (v-SETTINGS['min_bat_adc'])/( SETTINGS['max_bat_adc']-SETTINGS['min_bat_adc']) * 100;


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
            "{:03.0f},".format(get_battery()) + \
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
        connect_with_timeout(s, SETTINGS['rtt_server'], SETTINGS['rtt_port'], 10)
        print(get_rtt_string())
        s.write(get_rtt_string())
    finally:
        s.close()

def delay(ms):
    machine.set_idle(True)
    
    step = 10000

    while ms > 0:
        if ms < step:
            step = ms

        utime.sleep_ms(step)
        ms -= step
        machine.watchdog_reset()

    machine.set_idle(False)

def reset_gsm():
    cellular.reset()
    cellular.on_call(on_call_handler)
    cellular.on_status_event(network_handler)


def wait_gprs():
    while not cellular.gprs():
        machine.set_idle(True)

        iteration = 0

        led2.value(1)

        while not (cellular.get_network_status() & NTW_REG_BIT):
            delay(60000)
            iteration += 1

            if iteration > 5:
                reset_gsm()
                tm = 1

        led2.value(0)

        try:
            cellular.gprs(SETTINGS['apn'], SETTINGS['login'], SETTINGS['password'])
        except Exception as err:
            print("OS error: {0}".format(err));
            reset_gsm()

        machine.watchdog_reset()
        machine.set_idle(False)

def main_iteration():
    global led
    led.value(1)
    machine.watchdog_reset()

    try: 
        wait_gprs()
        machine.set_min_freq(machine.PM_SYS_FREQ_13M)
        send_rtt_coordinates()
    except Exception as err:
        print("OS error: {0}".format(err));
        try:
            cellular.SMS('+79169542241', "OS error: {0}".format(err)).send()
        except Exception as e:
            pass
    finally:
        machine.watchdog_reset()
        led.value(0)


def main_loop():
    while (True):
        set_gps_state(True)
        main_iteration()
        set_gps_state(False)
        delay(SETTINGS['track_delay_minutes'] * 60 * 1000)

reset_gsm()
machine.watchdog_on(120)
machine.set_min_freq(machine.PM_SYS_FREQ_13M)

main_loop()

