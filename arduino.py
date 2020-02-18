import serial
import random
from time import sleep

port = "COM9"
ser = serial.Serial(port,9600)
ser.flushInput()
ser.flushOutput()
while True:
    #new pyhton arduino! 
    HR=random.randint(1,200)
    RR=random.randint(500,1000)
    
    n1 = str(RR)
    n1 += "\r\n"

    n2 = str(HR)
    n2 += "\r\n"

    ser.write(n1.encode())
    ser.write(n2.encode())

    print ("HR es:",HR)
    print ("RR es:",RR)

    sleep(0.5)
ser.close()