#Author Justin Alderson
#The beginning of a home monitoring system.
#Built for Raspberry Pi. Needs to run as root. sudo motion_detector.py
#The program senses movements through a PIR sensor. A movement object
#is created with the count and datetime passed in, this is stored in
#a list. The list is saved to a file periodically. The program will
#also flash an LED to show it has detected movement.

import RPi.GPIO as GPIO
import time
import datetime
import pickle
import motion

#All variables are listed here.
GPIO_PIR = 7
GPIO_LED = 11
Current_State = 0
Previous_State = 0
count = 0
save_count = 0
oclock = 0
movement_detected = []

print("Home movement counter preparing to launch.")

#Setup GPIO for usage.
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_LED, GPIO.OUT)
GPIO.setup(GPIO_PIR, GPIO.IN)

#Save function will be called periodically.
def save():
    data = movement_detected
    save_file = open('/home/pi/Home_Monitor/data.dat','wb')
    pickle.dump(data, save_file)
    save_file.close()


#Try to load any previously stored data. If available assign to count and movement_detected.
try:
    load_file = open('/home/pi/Home_Monitor/data.dat', 'rb')
    data = pickle.load(load_file)
    movement_detected = data
    count = len(movement_detected)
    load_file.close()

except EOFError:
    pass

#Try used so that a KeyboardInterrupt can be used to stop progaram.
try:

    time.sleep(2)

    print("Launching.")

    while True:

        #Find the date and time.
        oclock = datetime.datetime.now()

        #Get the input from the PIR.
        Current_State = GPIO.input(GPIO_PIR)
        #Set LED off
        GPIO.output(11, 0)

        #Save at intervals of over 500 movements and on the 59th minute of the hour to prevent over saving.
        if save_count > 500 and oclock.minute == 59:
            save()
            #Reset save_count to start the next 500 counts until saving again.
            save_count = 0

        #If PIR detects something a 1 will be returned.
        if Current_State == 1:
           print "Motion %d " %count
           print(datetime.datetime.today())
           #Create Movement class object here.
           detected = motion.Movement(count,datetime.datetime.today())
           #Slight delay to allow system time.
           time.sleep(0.2)
           count += 1
           save_count += 1
           #LED on
           GPIO.output(11, 1)
           #Append Movement object to list.
           movement_detected.append(detected)

        #Slight delay to allow system time.
        time.sleep(0.2)

#Will accept Control C in the terminal to exit program. It will print Shutdown message.
except KeyboardInterrupt:
    #Save on shutdown of program to prevent any loss of data.
    save()
    print("Home Movement Detector Shutdown")
    GPIO.cleanup()
