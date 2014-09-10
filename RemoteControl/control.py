import RPi.GPIO as GPIO
import time
import math
 
GPIO.setmode(GPIO.BCM)

Motor1A = 16 #Left Fwd
Motor1B = 20 #Left Bwd
Motor1E = 21 #Left Enable
Motor2A = 19 #Right Fwd
Motor2B = 26 #Right Bwd
Motor2E = 13 #Right Enable

pwm1E = None
pwm2E = None

lastLeft = 0
lastRight = 0

def CarSetup():
    global pwm1E, pwm2E
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)
     
    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    GPIO.setup(Motor2E,GPIO.OUT)
    pwm1E = GPIO.PWM( Motor1E, 50 )
    pwm2E = GPIO.PWM( Motor2E, 50 )

    pwm1E.start( 100 )
    pwm2E.start( 100 )
    
def Move(right, left):
    global lastLeft, lastRight
    global pwm1E, pwm2E
    if lastLeft != left:
        pwm1E.ChangeDutyCycle(convert(left))
        if left > 0: # left move fwd
            GPIO.output(Motor1A, GPIO.HIGH)
            GPIO.output(Motor1B, GPIO.LOW)
            GPIO.output(Motor1E, GPIO.HIGH)
        elif left < 0: #left move bwd
            GPIO.output(Motor1B, GPIO.HIGH)
            GPIO.output(Motor1A, GPIO.LOW)
            GPIO.output(Motor1E, GPIO.HIGH)
        elif left == 0:
            GPIO.output(Motor1A, GPIO.LOW)
            GPIO.output(Motor1B, GPIO.LOW)
            GPIO.output(Motor1E, GPIO.LOW)
        lastLeft = left
    if lastRight != right:
        pwm2E.ChangeDutyCycle(convert(right))
        if right > 0: # left move fwd
            GPIO.output(Motor2A, GPIO.HIGH)
            GPIO.output(Motor2B, GPIO.LOW)
            GPIO.output(Motor2E, GPIO.HIGH)
        elif right < 0: #right move bwd
            GPIO.output(Motor2B, GPIO.HIGH)
            GPIO.output(Motor2A, GPIO.LOW)
            GPIO.output(Motor2E, GPIO.HIGH)
        elif right == 0:
            GPIO.output(Motor2A, GPIO.LOW)
            GPIO.output(Motor2B, GPIO.LOW)
            GPIO.output(Motor2E, GPIO.LOW)
        lastRight = right

            
def Cleanup():
    global pwm1E, pwm2E
    try:
        Move(0, 0)
        pwm1E.stop()
        pwm2E.stop()
    except:
        pass
    finally:
        GPIO.cleanup()
    
def convert(x):
    return math.fabs(100 * math.pow(float(x) / 128, 1))
    
def Test():
    Move(60, 20)
    time.sleep(0.1)
    Move(0, 128)
    time.sleep(0.1)
    Move(-20, -128)
    time.sleep(0.1)
    Move(-128, -20)
    time.sleep(0.1)
    Move(20, 20)
    time.sleep(0.1)
    Move(-20, -20)
    time.sleep(0.1)
    Move(0, 0)
    print "Test Completed"
