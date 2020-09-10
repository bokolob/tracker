from micropython import const
import time
import machine
from struct import unpack

# Register addresses:
# pylint: disable=bad-whitespace
_REG_OUT_T       = const(0x0C)
_REG_INFO1       = const(0x0D)
_REG_INFO2       = const(0x0E)
_REG_WHO_AM_I    = const(0x0F)
_REG_OFF_X       = const(0x10)
_REG_OFF_Y       = const(0x11)
_REG_OFF_Z       = const(0x12)
_REG_CS_X        = const(0x13)
_REG_CS_Y        = const(0x14)
_REG_CS_Z        = const(0x15)
_REG_LC_L        = const(0x16)
_REG_LC_H        = const(0x17)
_REG_STAT        = const(0x18)
_REG_PEAK1       = const(0x19)
_REG_PEAK2       = const(0x1A)
_REG_VFC_1 = const(0x1B)
_REG_VFC_2 = const(0x1C)
_REG_VFC_3 = const(0x1D)
_REG_VFC_4 = const(0x1E)
_REG_THRS3 = const(0x1F)
_REG_CTRL_REG4 = const(0x20)
_REG_CTRL_REG1 = const(0x21)
_REG_CTRL_REG2 = const(0x22)
_REG_CTRL_REG3 = const(0x23)
_REG_CTRL_REG5 = const(0x24)
_REG_CTRL_REG6 = const(0x25)
_REG_STATUS = const(0x27)
_REG_OUT_X_L = const(0x28)
_REG_OUT_X_H = const(0x29)
_REG_OUT_Y_L = const(0x2A)
_REG_OUT_Y_H = const(0x2B)
_REG_OUT_Z_L = const(0x2C)
_REG_OUT_Z_H = const(0x2D)
_REG_FIFO_CTRL = const(0x2E)
_REG_FIFO_SRC = const(0x2F)
#TODO _REG_ST1_X = const(0x40-4F)
_REG_TIM4_1 = const(0x50)
_REG_TIM3_1 = const(0x51)
#_REG_TIM2_1 = const(0x52-53)
#_REG_TIM1_1 = const(0x54-55)
_REG_THRS2_1 = const(0x56)
_REG_THRS1_1 = const(0x57)
_REG_MASK1_B = const(0x59)
_REG_MASK1_A = const(0x5A)
_REG_SETT1 = const(0x5B)
_REG_PR1 = const(0x5C)
#TODO _REG_TC1 = const(0x5D-5E)
_REG_OUTS1 = const(0x5F)
#TODO _REG_ST2_X = const(0x60-6F)
_REG_TIM4_2 = const(0x70)
_REG_TIM3_2 = const(0x71)
_REG_TIM2_2 = const(0x72-73)
#TODO_REG_TIM1_2 = const(0x74-75)
_REG_THRS2_2 = const(0x76)
_REG_THRS1_2 = const(0x77)
_REG_DES2 = const(0x78)
_REG_MASK2_B = const(0x79)
_REG_MASK2_A = const(0x7A)
_REG_SETT2 = const(0x7B)
_REG_PR2 = const(0x7C)
#TODO  _REG_TC2 = const(0x7D-7E)
_REG_OUTS2 = const(0x7F)

class LIS3DH:
    def __init__(self):
        # Check device ID.
        device_id = self._read_register_byte(_REG_WHO_AM_I)
        print(str(bin(device_id)))
        if device_id != 0x3F:
            raise RuntimeError('Failed to find LIS3DSH!')

        # Reboot
        self._write_register_byte(_REG_CTRL_REG6, 0x90) #reboot & add_inc
        time.sleep(0.01)  # takes 5ms

        self._write_register_byte(_REG_CTRL_REG4, 0x3f) #X, Y, Z enabled, ODR = 25 Hz, BDU enabled

    def accelleration(self):
        x = unpack('<h', self._read_register(_REG_OUT_X_L, 2))
        y = unpack('<h', self._read_register(_REG_OUT_Y_L, 2))
        z = unpack('<h', self._read_register(_REG_OUT_Z_L, 2))
        return (x,y,z)

    def _read_register(self, register, length):
        # Read an arbitrarily long register (specified by length number of
        # bytes) and return a bytearray of the retrieved data.
        # Subclasses MUST implement this!
        raise NotImplementedError

    def _write_register_byte(self, register, value):
        # Write a single byte register at the specified register address.
        # Subclasses MUST implement this!
        raise NotImplementedError

    def _read_register_byte(self, register):
        # Read a byte register value and return it.
        return self._read_register(register, 1)[0] & 0xFF


class LIS3SDH_SPI(LIS3DH):
    """Driver for the LIS3SDH accelerometer connected over SPI."""

    def __init__(self, spi, cs):
        self._cs = cs
        self._spi = spi
        self._addr_buf = bytearray(1)
        self._result8_buf = bytearray(1)
        self._result16_buf = bytearray(2)
        self._cs.value(1)
        super().__init__()

    def _read_register(self, register, length):
        out = None
        self._addr_buf[0] = (register | 0x80)  # Read single, bit 7 high.

        if length == 1:
            out = self._result8_buf
        else:
            out = self._result16_buf

        self._cs.value(0)
        self._spi.write(self._addr_buf) # pylint: disable=no-member
        self._spi.readinto(out) # pylint: disable=no-member
        self._cs.value(1)

        return out

    def _write_register_byte(self, register, value):
        self._result16_buf[0] = register & 0x7F  # Write, bit 7 low.
        self._result16_buf[1] = value & 0xFF
        self._cs.value(0)
        self._spi.write(self._result16_buf) # pylint: disable=no-member
        self._cs.value(1)

def main():
    scl=machine.Pin(19,machine.Pin.OUT, 1)
    sda=machine.Pin(20, machine.Pin.OUT, 0)
    sdo=machine.Pin(15, machine.Pin.IN, 0)
    cs=machine.Pin(14, machine.Pin.OUT,1)

    spi = machine.SPI(-1, sck=scl, miso=sdo, mosi=sda)
    spi.init(400000, polarity=0, phase=0)

    return LIS3SDH_SPI(spi, cs)



