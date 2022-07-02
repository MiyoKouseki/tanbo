import smbus
import wiringpi
import os
import struct
import time


class Hdc1000():
    def __init__(self):
        wiringpi.wiringPiSetup()
        self.i2c = wiringpi.I2C()
        self.setup()
        
    def setup(self):
        self.dev = self.i2c.setup(0x40)
        # 温度と湿度を14bitで読む設定にする        
        self.i2c.writeReg16(self.dev,0x02,0x10) 
        self.i2c.writeReg8(self.dev,0x00,0x00) # 開始
        time.sleep((6350.0 + 6500.0 + 500.0)/1000000.0)

    def read_temp_and_humid(self):
        temp = ((struct.unpack('4B', os.read(self.dev,4)))[0] << 8 | (struct.unpack('4B', os.read(self.dev,4)))[1])
        hudi = ((struct.unpack('4B', os.read(self.dev,4)))[2] << 8 | (struct.unpack('4B', os.read(self.dev,4)))[3])
        os.close(self.dev)
        temp = (temp / 65535.0) * 165 - 40 
        humid = ( hudi / 65535.0 ) * 100
        return temp,humid


class Adt7410():
    def __init__(self):
        self.i2c = smbus.SMBus(1)
        self.address = 0x48
        self.setup()
        
    def setup(self):
        ret = self.i2c.write_byte_data(self.address, 0x03, 0x80)
        
    def read_temp(self):
        data = self.i2c.read_word_data(self.address, 0x00)
        data = (data & 0xFF00) >> 8 | (data & 0x00FF) << 8
        data = data >> 3
        temp = data*0.0625
        return temp



    
if __name__=="__main__":
    sens1 = Adt7410()
    temp1 = sens1.read_temp()
    sens2 = Hdc1000()
    temp2,humid2 = sens2.read_temp_and_humid()    
    print('温度(ADT7410)：%2.1f 度'%(temp1))
    print('温度(HDC1000)：%2.1f 度'%(temp2))    
