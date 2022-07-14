


if __name__=='__main__':
    import time
    import board
    import adafruit_ina260
    from datetime import datetime
    i2c = board.I2C()
    txt = "{:26s},{:>5},{:>5},{:>5}".format("Time[JST]","ch0 [V]","ch1 [V]","ch2 [V]")
    with open('ina260.dat','w') as f:
        print(txt)
        f.write(txt+'\n')        
    while True:
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        try:
            ch0 = adafruit_ina260.INA260(i2c,address=0x42) # battery
            v0 = ch0.voltage
        except:
            v0 = 0
        try:
            ch1 = adafruit_ina260.INA260(i2c,address=0x4c) # pannel     
            v1 = ch1.voltage
        except:
            v1 = 0
        try:
            ch2 = adafruit_ina260.INA260(i2c,address=0x43) # load
            v2 = ch2.voltage
        except:
            v2 = 0
        txt = "{:26s},{:>5.4f},{:>5.4f},{:>5.4f}".\
            format(now,v0,v1,v2)
        print(txt)
        with open('ina260.dat','a') as f:
            f.write(txt+'\n')    
        time.sleep(10*60)        
