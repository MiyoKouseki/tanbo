import RPi.GPIO as GPIO
from sr04 import Sr04
from datetime import datetime
import time

def read_distance():
    try:    
        dis = 0
        ave,duty = 3,0.01
        for num in range(ave):
            sens3 = Sr04()                
            dis += sens3.calc_distance(duty=0.05)
        dis /= ave
        return dis
    finally:
        GPIO.cleanup()
        
if __name__=='__main__':
    f = open('waterheight.dat','w')
    txt = "#datetime,distance[cm]\n"
    f.write(txt)
    while True:
        try:
            dis = read_distance()
            now = datetime.now()
            now_str = now.strftime('%Y-%m-%dT%H:%M:%S.%f')
            txt = "%s,%4.1f"%(now_str,dis)
            print(txt)
            f.write(txt+'\n')
            time.sleep(1)
        except KeyboardInterrupt:
            f.close()
