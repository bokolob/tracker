import utime
import machine

class SoftI2C:
    sda=None
    scl=None
    delay = 1

    def __init__(self, scl=machine.Pin(20), sda=machine.Pin(19), delay=10):
        self.scl=scl
        self.sda=sda
        self.delay=delay
        self.sdaHi()
        self.sclHi()
    

    def i2cDelay(self):
        utime.sleep_us(self.delay)


    def sclHi(self):
        self.scl.init(machine.Pin.IN, 1)
        
        while self.scl.value() != 1:
            continue

        self.i2cDelay();


    def sdaHi(self):
        self.sda.init(machine.Pin.IN, 1)
        self.i2cDelay()
    

    def sclLo(self):
        self.scl.init(machine.Pin.OUT, 0)
        self.i2cDelay()


    def sdaLo(self):
        self.sda.init(machine.Pin.OUT, 0)
        self.i2cDelay()


    def start(self):
        self.sdaHi();
        self.sclHi();
        self.i2cDelay();
        self.sdaLo();
        self.i2cDelay();
        self.sclLo();
        self.i2cDelay();


    def stop(self):
        self.sdaLo();
        self.i2cDelay();
        self.sclHi();
        self.i2cDelay();
        self.sdaHi();
        self.i2cDelay();
    

    def clockPulse(self):
        self.sclHi();
        self.i2cDelay();
        self.sclLo();


    def writeByte(self, data_byte):
        for i in range(8):
            if data_byte & (1 << 7-i):
                self.sdaHi()
            else:
                self.sdaLo()

            self.clockPulse()


    def writeNack(self):
        self.sdaHi()
        self.clockPulse()

    def writeAck(self):
        self.sdaLo()
        self.clockPulse()

    def readBit(self):
        self.sclHi()
        out_bit = self.sda.value()
        self.sclLo()

        return out_bit


    def readByte(self):
        out_byte = 0
        self.sdaHi()
        for i in range(8):
            if self.readBit():
                out_byte |= (1 << 7 - i)
            else:
                out_byte &= ~(1 << 7 - i)

        return out_byte;


    def readAck(self):
        self.sdaHi()
        return self.readBit() # 0 if ACK, 1 if NACK

    def doStartWriteAckStop(self, data_byte):
        self.start()
        self.writeByte(data_byte);

        if self.readAck():
            return 1;

        self.stop();

        return 0


    def readRegister(self, slave_addr, register):
        result = self.readSequence(slave_addr, register, 1)
        return result[0]


    def readSequence(self, slave_addr, register, length):
        self.start();
        self.writeByte(slave_addr << 1);
        self.readAck();
        self.writeByte(register)
        self.readAck()
        self.start()
        self.writeByte(slave_addr << 1 | 0x1)
        self.readAck()

        result = []

        while length > 0:
            result.append(self.readByte())

            if length != 1:
                self.writeAck()

            length = length - 1

        self.writeNack()
        self.stop()
        return result


    def writeRegister(self, slave_addr, register, value):
        self.start();
        self.writeByte(slave_addr << 1);
        self.readAck()
        self.writeByte(register)
        self.readAck()
        self.writeByte(value)
        self.readAck()
        self.stop()

