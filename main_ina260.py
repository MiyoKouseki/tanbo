#!/usr/bin/python3

import time
import signal
import board
import adafruit_ina260
from datetime import datetime
    
def main(arg1, args2):
    i2c = board.I2C()
    txt = "{:26s},{:>5},{:>5},{:>5}".format("Time[JST]","ch0[V]","ch1[V]","ch2[V]") \
        + ",{:>5},{:>5},{:>5}".format("ch0[A]","ch1[A]","ch2[A]") \
        + ",{:>5},{:>5},{:>5}".format("ch0[W]","ch1[W]","ch2[W]")        
    # with open('ina260.dat','w') as f:
    #     print(txt)
    #     f.write(txt+'\n')        
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    # try:
    #     ch0 = adafruit_ina260.INA260(i2c,address=0x42) # pannel
    #     v0 = ch0.voltage
    #     i0 = ch0.current/1000
    #     p0 = ch0.power/1000        
    # except:
    #     v0 = 0
    #     i0 = 0
    #     p0 = 0
    v0 = 0
    i0 = 0
    p0 = 0
    
    try:
        ch1 = adafruit_ina260.INA260(i2c,address=0x4c) # load
        v1 = ch1.voltage
        i1 = ch1.current/1000
        p1 = ch1.power/1000                  
    except:
        v1 = 0
        i1 = 0
        p1 = 0            
    try:
        ch2 = adafruit_ina260.INA260(i2c,address=0x43) # battery
        v2 = ch2.voltage
        i2 = ch2.current/1000
        p2 = ch2.power/1000
        if i2>0:
            p2 = p2*-1        
    except:
        v2 = 0
        i2 = 0
        p2 = 0            
    txt = "{:26s},{:>+6.3f},{:>+6.3f},{:>+6.3f}".format(now,v0,v1,v2) \
        + ",{:>+6.3f},{:>+6.3f},{:>+6.3f}".format(i0,i1,i2) \
        + ",{:>+6.3f},{:>+6.3f},{:>+6.3f}".format(p0,p1,p2)
    print(txt)
    with open('/home/pi/play/tanbo/ina260.dat','a') as f:
        f.write(txt+'\n')        

if __name__=='__main__':
    signal.signal(signal.SIGALRM, main)
    signal.setitimer(signal.ITIMER_REAL, 10, 10)
    while True:
        pass
