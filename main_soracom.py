import json
import requests
import subprocess
import board
import adafruit_ina260
from sensors import Adt7410,Hdc1000

def get_voltage():
    i2c = board.I2C()
    ch0 = adafruit_ina260.INA260(i2c,address=0x42) # battery
    v0,i0,p0 = ch0.voltage,ch0.current,ch0.power
    ch1 = adafruit_ina260.INA260(i2c,address=0x4c) # pannel     
    v1,i1,p1 = ch1.voltage,ch1.current,ch1.power    
    ch2 = adafruit_ina260.INA260(i2c,address=0x43) # load
    v2,i2,p2 = ch2.voltage,ch2.current,ch2.power        
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
        'battery_voltage':v0,
        'solar_voltage':v1,
        'load_voltage':v2,
        'battery_current':i0,
        'solar_current':i1,
        'load_current':i2,
        'battery_power':p0,
        'solar_power':p1,
        'load_power':p2,        
    }    
    res = requests.post('http://harvest.soracom.io',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    print(res,cputemp,box_temp)
