import cellular
import machine
import utime

from delay import delay
from settings import get_property

callbacks = None
led2 = machine.Pin(28, machine.Pin.OUT, 0)


class Callbacks:
    sms_handler = None
    call_handler = None
    network_handler = None

    def __init__(self):
        return


def set_callbacks(ref):
    global callbacks
    callbacks = ref


def reset_gsm():
    cellular.reset()
    init()


def init():
    while not cellular.is_sim_present():
        print("No sim card..")
        utime.sleep_ms(1000)

    cellular.on_new_sms(callbacks.sms_handler)
    cellular.on_call(callbacks.call_handler)
    cellular.on_status_event(callbacks.network_handler)


def wait_gprs():
    while not cellular.gprs():
        machine.set_idle(True)

        iteration = 0

        led2.value(1)

        while not cellular.is_network_registered():
            delay.delay(60000)
            iteration += 1

            if iteration > 5:
                reset_gsm()
                tm = 1

        led2.value(0)

        try:
            cellular.gprs(get_property('apn'), get_property('login'), get_property('password'))
        except Exception as err:
            print("OS error: {0}".format(err));
            reset_gsm()

        machine.watchdog_reset()
        machine.set_idle(False)
