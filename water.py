# External module imp
import RPi.GPIO as GPIO
import datetime
import time

init = False

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setwarnings(False)

def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.read()
    except:
        return "NEVER!"
      
def get_status(pin = 8):
    GPIO.setup(pin, GPIO.IN) 
    return GPIO.input(pin)

def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)
    

def auto_water(pump_pin = 7, water_sensor_pin = 8, count = 0):
    print("turn on auto water. CTRL+C to exit")
    try:
        while 1:
            if get_status(water_sensor_pin) :
                init_output(pump_pin)
                if count == 10000:
                    pump_on()
                    count += 1
                else:
                    count += 1
            else:
                power_off()
                count = 0
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPIexce
        
def pump_on(pin = 7):
    f = open("last_watered.txt", "a+")
    f.write("-----------------------------------------------------Last watered {} ---------------------------------------------\n".format(datetime.datetime.now()))
    f.close()
    init_output(pin)

def power_off():
	GPIO.setup(7, GPIO.OUT)
	GPIO.output(7, GPIO.LOW)
