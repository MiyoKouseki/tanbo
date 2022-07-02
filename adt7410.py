import smbus

i2c = smbus.SMBus(1)
address = 0x48
ret = i2c.write_byte_data(address, 0x03, 0x80)
data = i2c.read_word_data(address, 0x00)
data = (data & 0xFF00) >> 8 | (data & 0x00FF) << 8
data = data >> 3
data *= 0.0625
print('温度(ADT7410)：%2.1f 度'%(data))
