import RPi.GPIO as io
import time

io.setmode(io.BCM)

trigger = 8
echo = 25
buzzer = 15

io.setup(buzzer, io.OUT)
io.setup(trigger, io.OUT)
io.setup(echo, io.IN)

pwm = io.PWM(buzzer, 50)
dc = 0
pwm.start(dc)
minRange = 0
maxRange = 30

def distance():
    io.output(trigger, True)
    time.sleep(0.00001)
    io.output(trigger, False)
    
    startTime = time.time()
    stopTime = time.time()
    
    while io.input(echo) == 0:
        startTime = time.time()
    
    while io.input(echo) == 1:
        stopTime = time.time()
        
    timeElapsed = stopTime - startTime
    distance = timeElapsed*34300/2
    return distance

if __name__ == '__main__':
    try:
        while True:
            d = distance()
            print("Distance = %.0f cm" %d)
            if (d <= maxRange):
                dc = 100 - round(d/maxRange*100)
                print("Duty = %d"%dc)
                pwm.ChangeDutyCycle(dc)
            else:
                pwm.ChangeDutyCycle(0)
                print("Out of range")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped")  
        io.cleanup()          