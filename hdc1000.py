import wiringpi
import os
import struct
import time
wiringpi.wiringPiSetup()
i2c = wiringpi.I2C() 
dev = i2c.setup(0x40)
i2c.writeReg16(dev,0x02,0x10) # 温度と湿度を14bitで読む設定にする
i2c.writeReg8(dev,0x00,0x00) # 開始
time.sleep((6350.0 + 6500.0 + 500.0)/1000000.0)
temp = ((struct.unpack('4B', os.read(dev,4)))[0] << 8 | (struct.unpack('4B', os.read(dev,4)))[1])
hudi = ((struct.unpack('4B', os.read(dev,4)))[2] << 8 | (struct.unpack('4B', os.read(dev,4)))[3])
os.close(dev)
print("温度(HDC1000): %.1f 度" % (( temp / 65535.0) * 165 - 40 ))
#print("湿度?: %.1f %%" % (( hudi / 65535.0 ) * 100))

