import json
import requests
import subprocess
import board
import adafruit_ina260
from sensors import Adt7410,Hdc1000
from datetime import datetime

# def get_voltage():
#     i2c = board.I2C()
#     ch0 = adafruit_ina260.INA260(i2c,address=0x42) # solar
#     v0,i0,p0 = ch0.voltage,ch0.current/1000,ch0.power/1000
#     ch1 = adafruit_ina260.INA260(i2c,address=0x4c) # load     
#     v1,i1,p1 = ch1.voltage,ch1.current/1000,ch1.power/1000
#     ch2 = adafruit_ina260.INA260(i2c,address=0x43) # battery    
#     v2,i2,p2 = ch2.voltage,ch2.current/1000,ch2.power/1000
#     if i2>0:
#         p2 = p2*-1
#     return v0,v1,v2,i0,i1,i2,p0,p1,p2

def get_voltage():
    i2c = board.I2C()
    try:
        ch0 = adafruit_ina260.INA260(i2c,address=0x42) # solar
        v0,i0,p0 = ch0.voltage,ch0.current/1000,ch0.power/1000
    except:
        v0,i0,p0 = 0,0,0
    try:
        ch1 = adafruit_ina260.INA260(i2c,address=0x4c) # load     
        v1,i1,p1 = ch1.voltage,ch1.current/1000,ch1.power/1000
    except:
        v1,i1,p1 = 0,0,0
    try:
        ch2 = adafruit_ina260.INA260(i2c,address=0x43) # battery    
        v2,i2,p2 = ch2.voltage,ch2.current/1000,ch2.power/1000
    except:
        v0,i0,p0 = 0,0,0
        
    if i2>0:
        p2 = p2*-1
    return v0,v1,v2,i0,i1,i2,p0,p1,p2        

def get_health():
    cmd = 'bash check.sh | grep temp'
    res = subprocess.run(cmd,shell=True,
                         encoding='utf-8',
                         stdout=subprocess.PIPE)
    cputemp = float(res.stdout.split('=')[1].replace("'C",''))
    # -----
    cmd = 'bash check.sh | grep frequency'
    res = subprocess.run(cmd,shell=True,
                         encoding='utf-8',
                         stdout=subprocess.PIPE)
    clock = float(res.stdout.split('=')[1])
    # -----
    cmd = 'bash check.sh | grep throttled'
    res = subprocess.run(cmd,shell=True,
                         encoding='utf-8',
                         stdout=subprocess.PIPE)
    pw_health = res.stdout.split('=')[1].replace('\n','')    
    return cputemp,clock,pw_health

def get_temp():
    sens2 = Hdc1000()
    temp2,humid2 = sens2.read_temp_and_humid()
    return temp2

if __name__ == "__main__":
    v0,v1,v2,i0,i1,i2,p0,p1,p2 = get_voltage()
    cputemp,clock,pw_health = get_health()
    box_temp = get_temp()
    data = {
        'box_temp':box_temp,
        'cpu_temp':cputemp,
        'clock':clock,
        'solar_voltage':v0,
        'load_voltage':v1,
        'battery_voltage':v2,
        'solar_current':i0,
        'load_current':i1,
        'battery_current':i2,
        'solar_power':p0,
        'load_power':p1,
        'battery_power':p2,        
    }    
    res = requests.post('http://harvest.soracom.io',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    print(now,res,cputemp,box_temp)
