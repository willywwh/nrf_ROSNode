#!/usr/bin/env python2

#/////// Import Section ////////////#
import rospy
from std_msgs.msg import UInt8MultiArray
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
#/////////////////////////////////#
#//////////// Variables //////////#
global radio
global radioData
global genericAngle
global throttle # Throttle range is mapped from 1000 - 2000 to 100 to 200 to be transmitted as a byte
global flareFlag # No flare as it is inverted
global commLoss
#/////////////////////////////////#
#/////////// NRF Setup ///////////#
def nrfSetup():
    global radio
    GPIO.setmode(GPIO.BCM)
    pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
    radio = NRF24(GPIO,spidev.SpiDev())
    radio.begin(0,17)
    radio.setPayloadSize(32)
    radio.setChannel(0x76)
    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setPALevel(NRF24.PA_MAX)
    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()
    radio.openReadingPipe(1,pipes[1])
    radio.printDetails()
    radio.startListening()
#//////////////////////////////////#

def correctRadio():
    global genericAngle
    global throttle # Throttle range is mapped from 1000 - 2000 to 100 to 200 to be transmitted as a byte
    global flareFlag  # No flare as it is inverted
    if genericAngle < 0 or genericAngle > 200 or throttle < 100 or throttle > 200:
        genericAngle = 100
        throttle = 100
        flareFlag = True

def radioReceive():
    global radioData
    global genericAngle
    global throttle # Throttle range is mapped from 1000 - 2000 to 100 to 200 to be transmitted as a byte
    global flareFlag # No flare as it is inverted
    global autonomousFlag
    global commLoss

    radioData = []
    if radio.available(0):
        radio.read(radioData, radio.getDynamicPayloadSize())
        genericAngle = radioData[0]
        throttle = radioData[1]
        flareFlag = radioData[2]
        autonomousFlag = radioData[3]
        commLoss = False
    else:
        genericAngle = 100
        throttle = 100 # Throttle range is mapped from 1000 - 2000 to 100 to 200 to be transmitted as a byte
        flareFlag = False
        autonomousFlag = False
        commLoss = True
    correctRadio()


def nrfPublisher():
    nrfSetup()
    nrfPub = rospy.Publisher('radioControlSignal', UInt8MultiArray, queue_size=5)
    rospy.init_node('nrfPublisher', anonymous=True)
    rate = rospy.Rate(20) # 20hz
    radioMsg = UInt8MultiArray()
    radioMsg.layout.data_offset = 4
    while not rospy.is_shutdown():
        radioReceive()
        radioMsg.data = [genericAngle,throttle,flareFlag,autonomousFlag]
	nrfPub.publish(radioMsg)        
	rate.sleep()

if __name__ == '__main__':
        nrfPublisher()
   
