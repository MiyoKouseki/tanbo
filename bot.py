#!/usr/bin/python3
import subprocess
import discord
from secrets import TOKEN
from sensors import Adt7410,Hdc1000
from datetime import datetime
import board
import adafruit_ina260
from datetime import datetime
    
# python3 -m pip install -U "discord.py"


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
        v0,i0,p0 = 0,0,0
    try:
        ch2 = adafruit_ina260.INA260(i2c,address=0x43) # battery    
        v2,i2,p2 = ch2.voltage,ch2.current/1000,ch2.power/1000
    except:
        v0,i0,p0 = 0,0,0
        
    if i2>0:
        p2 = p2*-1
    return v0,v1,v2,i0,i1,i2,p0,p1,p2        

def main():
    _temp2 = 0
    _cputemp = 0
    _pw_health = 'none'
    _clock = '0'            
    _v0,_v1,_v2 = 0,0,0
    
    client = discord.Client()
    
    # 起動時に動作する処理
    @client.event
    async def on_ready():
        print('ログインしました')

    # メッセージ受信時に動作する処理
    @client.event
    async def on_message(message):
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return
        if '/tanbo' in message.content:
            if '/tanbo show'==message.content:
                cmd = 'fswebcam -p YUYV -r 320x240 -F 3 -S 20 '\
                    'now.png'
                res = subprocess.run(cmd,shell=True)
                with open('now.png', "rb") as fh:
                    f = discord.File(fh, filename='now.png')
                await message.channel.send(file=f)
            if '/tanbo health'==message.content:                
                sens2 = Hdc1000()
                temp2,humid2 = sens2.read_temp_and_humid()
                now = datetime.today()
                now_str = now.strftime('%Y-%m-%d %H:%M:%S')
                txt = now_str +'\n'                
                txt += " - 筐体温度['C]: {:>3.2f}\n".format(temp2)
                cmd = 'bash check.sh | grep temp'
                res = subprocess.run(cmd,shell=True,
                                     encoding='utf-8',
                                     stdout=subprocess.PIPE)
                cputemp = float(res.stdout.split('=')[1].replace("'C",''))
                txt += " - CPU温度['C]: {:>3.2f}\n".format(cputemp)
                cmd = 'bash check.sh | grep frequency'
                res = subprocess.run(cmd,shell=True,
                                     encoding='utf-8',
                                     stdout=subprocess.PIPE)
                clock = float(res.stdout.split('=')[1])
                txt += ' - クロック[Hz]: {:>3.2e}\n'.format(clock)
                cmd = "df -h | grep root | awk '{print $5}'"
                res = subprocess.run(cmd,shell=True,
                                     encoding='utf-8',
                                     stdout=subprocess.PIPE)                
                txt += " - SDカード使用率: {:>s}".format(res.stdout)                
                cmd = 'bash check.sh | grep throttled'
                res = subprocess.run(cmd,shell=True,
                                     encoding='utf-8',
                                     stdout=subprocess.PIPE)
                pw_health = res.stdout.split('=')[1].replace('\n','')
                txt += ' - 電源診断: {:>s}\n'.format(pw_health)
                v0,v1,v2,i0,i1,i2,p0,p1,p2 = get_voltage()
                txt += " - 太陽電池[W]: {:>5.2f}\n".format(p0)
                txt += " - 負荷[W]: {:>5.2f}\n".format(p1)
                txt += " - バッテリー[W]: {:>5.2f}\n".format(p2)
                txt += " - バッテリー[V]: {:>5.2f}\n".format(v2)                
                _temp2 = temp2
                _cputemp = cputemp
                _pw_health = pw_health
                _clock = clock                
                _v0,_v1,_v2 = v0,v1,v2
                await message.channel.send(txt)
            if '/tanbo voltage'==message.content:
                await message.channel.send(txt)                
                
                        
    client.run(TOKEN)


if __name__=='__main__':
    main()
