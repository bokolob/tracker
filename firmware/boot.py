import time

import cellular
import machine

# Built-in blue LED on the pudding board
cellular.on()
led = machine.Pin(27, machine.Pin.OUT, 1)
time.sleep(1)
led.value(0)

cellular.SMS('+79169542241', "System started").send()
