import cellular
import machine
import utime

import gprs
import location
from settings import get_property

interrupt=False;

def delay(ms, predicate=lambda:False):
    global interrupt
    machine.set_idle(True)

    step = 1000
    prev_gps_state = location.gps_state
    
    if get_property('disable_gprs_while_sleep'):
        cellular.gprs(False);
    
    if get_property('disable_gps_while_sleep'):
        location.set_gps_state(False)

    interrupt=False

    while ms > 0 and not predicate() and not interrupt:
        if ms < step:
            step = ms

        utime.sleep_ms(step)
        ms -= step
        machine.watchdog_reset()
    
    interrupt=False
    location.set_gps_state(prev_gps_state)
    machine.set_idle(False)
