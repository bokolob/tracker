import time
from struct import unpack

import machine
from micropython import const

# Register addresses:
# pylint: disable=bad-whitespace
OUT_T = const(0x0C)
INFO1 = const(0x0D)
INFO2 = const(0x0E)
WHO_AM_I = const(0x0F)
OFF_X = const(0x10)
OFF_Y = const(0x11)
OFF_Z = const(0x12)
CS_X = const(0x13)
CS_Y = const(0x14)
CS_Z = const(0x15)
LC_L = const(0x16)
LC_H = const(0x17)
STAT = const(0x18)
PEAK1 = const(0x19)
PEAK2 = const(0x1A)
VFC_1 = const(0x1B)
VFC_2 = const(0x1C)
VFC_3 = const(0x1D)
VFC_4 = const(0x1E)
THRS3 = const(0x1F)
CTRL_REG4 = const(0x20)
CTRL_REG1 = const(0x21)
CTRL_REG2 = const(0x22)
CTRL_REG3 = const(0x23)
CTRL_REG5 = const(0x24)
CTRL_REG6 = const(0x25)
STATUS = const(0x27)
OUT_X_L = const(0x28)
OUT_X_H = const(0x29)
OUT_Y_L = const(0x2A)
OUT_Y_H = const(0x2B)
OUT_Z_L = const(0x2C)
OUT_Z_H = const(0x2D)
FIFO_CTRL = const(0x2E)
FIFO_SRC = const(0x2F)
ST1_1 = const(0x40)
ST1_2 = const(0x41)
# TODO _REG_ST1_X = const(0x40-4F)
TIM4_1 = const(0x50)
TIM3_1 = const(0x51)
# _REG_TIM2_1 = const(0x52-53)
# _REG_TIM1_1 = const(0x54-55)
THRS2_1 = const(0x56)
THRS1_1 = const(0x57)
MASK1_B = const(0x59)
MASK1_A = const(0x5A)
SETT1 = const(0x5B)
PR1 = const(0x5C)
# TODO _REG_TC1 = const(0x5D-5E)
OUTS1 = const(0x5F)
# TODO _REG_ST2_X = const(0x60-6F)
TIM4_2 = const(0x70)
TIM3_2 = const(0x71)
TIM2_2 = const(0x72)  # 0x72-73
# TODO_REG_TIM1_2 = const(0x74-75)
THRS2_2 = const(0x76)
THRS1_2 = const(0x77)
DES2 = const(0x78)
MASK2_B = const(0x79)
MASK2_A = const(0x7A)
SETT2 = const(0x7B)
PR2 = const(0x7C)
# TODO  _REG_TC2 = const(0x7D-7E)
OUTS2 = const(0x7F)

WAKE_UP = (
    (CTRL_REG1, 0x01),
    (CTRL_REG3, 0x8),
    (CTRL_REG4, 0x67),
    (CTRL_REG5, 0x00),
    (THRS1_1, 0x55),
    (ST1_1, 0x05),
    (ST1_2, 0x11),
    (MASK1_B, 0xFC),
    (MASK1_A, 0xFC),
    (SETT1, 0x1)
)


class LIS3DH:
    def __init__(self):
        # Check device ID.
        device_id = self._read_register_byte(WHO_AM_I)
        print(str(hex(device_id)))
        if device_id != 0x3F:
            raise RuntimeError('Failed to find LIS3DSH!')

        # Reboot
        self._write_register_byte(CTRL_REG6, 0x90)  # reboot & add_inc
        time.sleep(0.01)  # takes 5ms

        self._write_register_byte(CTRL_REG4, 0x3f)  # X, Y, Z enabled, ODR = 25 Hz, BDU enabled

    def set_wake_up(self):
        for pair in WAKE_UP:
            self._write_register_byte(pair[0], pair[1]);

    def accelleration(self):
        x = unpack('<h', self._read_register(OUT_X_L, 2))
        y = unpack('<h', self._read_register(OUT_Y_L, 2))
        z = unpack('<h', self._read_register(OUT_Z_L, 2))
        return (x, y, z)

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


class LIS3DSH_SOFTI2C(LIS3DH):
    def __init__(self, soft_i2c, sel=1):
        self._i2c = soft_i2c

        if sel == 1:
            self.addr = 0b00011101
        else:
            self.addr = 0b00011110

        super().__init__()

    def _read_register(self, register, length):
        return bytearray(self._i2c.readSequence(self.addr, register, length))

    def _write_register_byte(self, register, value):
        return self._i2c.writeRegister(self.addr, register, value)


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
        self._spi.write(self._addr_buf)  # pylint: disable=no-member
        self._spi.readinto(out)  # pylint: disable=no-member
        self._cs.value(1)

        return out

    def _write_register_byte(self, register, value):
        self._result16_buf[0] = register & 0x7F  # Write, bit 7 low.
        self._result16_buf[1] = value & 0xFF
        self._cs.value(0)
        self._spi.write(self._result16_buf)  # pylint: disable=no-member
        self._cs.value(1)


def main():
    scl = machine.Pin(15, machine.Pin.OUT, 1)
    sda = machine.Pin(14, machine.Pin.OUT, 0)
    sdo = machine.Pin(17, machine.Pin.IN, 0)
    cs = machine.Pin(18, machine.Pin.OUT, 1)

    spi = machine.SPI(-1, sck=scl, miso=sdo, mosi=sda)
    spi.init(400000, polarity=0, phase=0)

    return LIS3SDH_SPI(spi, cs)
