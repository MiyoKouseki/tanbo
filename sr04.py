import RPi.GPIO as GPIO
import time

LOW,HIGH = 0,1
SPEED_OF_SOUND = 34000 # cm/sec
DUTY = 0.1
TRIG_PIN = 23
ECHO_PIN = 24

class Sr04Error(Exception):
    pass

class Sr04():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG_PIN,GPIO.OUT)
        GPIO.setup(ECHO_PIN,GPIO.IN)
        GPIO.setwarnings(False)

    def calc_distance(self,**kwargs):
        ''' 
        TRIGから矩形波を出して、対象物から反射した信号のONとOFFの
        時間差をECHOで測り、音速をつかって距離を計算する。
        '''
        duty = kwargs.get('duty',DUTY)
        self.put_trigger_sound(duty) 
        dt = self.get_delaytime()
        distance = SPEED_OF_SOUND * dt/2
        GPIO.cleanup()
        return distance

    def put_trigger_sound(self,duty=DUTY):
        '''
        TRIGから矩形波の音を出す
        '''
        # fixme: 常時出してもいい気がする        
        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(duty)
        GPIO.output(TRIG_PIN, HIGH)
        time.sleep(duty)
        GPIO.output(TRIG_PIN, LOW)
    
    def get_delaytime(self):
        '''
        ECHOがLOWからHIGHになる時間を測る
        '''
        # fixme: time.time は使いたくないな
        t_start,t_end = 0,0
        while GPIO.input(ECHO_PIN)==LOW:
            t_start = time.time() 
        while GPIO.input(ECHO_PIN)==HIGH:
            t_end = time.time()
        return t_end - t_start   


if __name__=="__main__":
    try:
        # fixme: ave*(duty*2) 程度、測定に時間がかかる?
        dis = 0
        ave,duty = 3,0.01
        for num in range(ave):
            sens3 = Sr04()                
            dis += sens3.calc_distance(duty=0.05)
        dis /= ave
        txt = '-'*int(dis)
        print("%f %5.1f cm %s"%(time.time(),dis,txt))
    except KeyboardInterrupt:
        GPIO.cleanup()          
        exit()
