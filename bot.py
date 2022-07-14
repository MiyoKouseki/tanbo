import subprocess
import discord
from secrets import TOKEN
from sensors import Adt7410,Hdc1000
from datetime import datetime
import board
import adafruit_ina260
from datetime import datetime
    
# python3 -m pip install -U "discord.py"

def main():    
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
            if '/tanbo temp'==message.content:
                sens1 = Adt7410()                
                temp1 = sens1.read_temp()
                sens2 = Hdc1000()
                temp2,humid2 = sens2.read_temp_and_humid()
                now = datetime.today()
                now_str = now.strftime('%Y-%m-%d %H:%M:%S')
                txt = now_str +'\n'+\
                    '温度(ADT7410): %2.1f 度\n'%(temp1) +\
                    '温度(HDC1000): %2.1f 度\n'%(temp2)
                await message.channel.send(txt)
            if '/tanbo voltage'==message.content:        
                i2c = board.I2C()
                ch0 = adafruit_ina260.INA260(i2c,address=0x42) # battery
                v0 = ch0.voltage
                ch1 = adafruit_ina260.INA260(i2c,address=0x4c) # pannel     
                v1 = ch1.voltage
                ch2 = adafruit_ina260.INA260(i2c,address=0x43) # load
                v2 = ch2.voltage
                txt = "{:>5.4f},{:>5.4f},{:>5.4f}".format(v0,v1,v2)
                await message.channel.send(txt)                
                
                        
    client.run(TOKEN)


if __name__=='__main__':
    main()
