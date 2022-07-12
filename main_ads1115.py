from datetime import datetime
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)


print("{:26s},{:>5},{:>5},{:>5}".format("Time[JST]","ch0[V]","ch1[V]","ch2[V]"))

while True:
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    v0 = chan0.voltage*5
    v1 = chan1.voltage*5    
    v2 = chan2.voltage*5
    v3 = chan3.voltage*5        
    print("{:26s},{:>5.4f},{:>5.4f},{:>5.4f},{:>5.4f}".format(now,v0,v1,v2,v3))
    time.sleep(1)
