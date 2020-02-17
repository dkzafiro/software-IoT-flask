import serial
import random
from time import sleep

port = "COM9"
ser = serial.Serial(port,9600)
while True:
    HR=random.randint(1,200)
    ser.write(str(HR))
    print "HR es:",HR
    #print "puerto":,ser.portstr
    sleep(1.5)
ser.close()