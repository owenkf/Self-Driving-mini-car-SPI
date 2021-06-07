import time
import cv2
import numpy as np
from picamera import PiCamera
import spidev

with PiCamera() as src:
    src.resolution = (640,640)
    src.framerate  = 30
    src.shutter_speed = 75000
    time.sleep(2)
    output = np.empty((450, 640,3), dtype=np.uint8)
    while(True):
        start_time = time.time()
        src.capture(output, format='bgr', use_video_port=True)
        #convert cam image to black and white
        gray = cv2.cvtColor(ouput, cv2.COLOR_BGR2GRAY)
        gray[gray < 50] = 0
        gray[gray > 50] = 255
        #find the black values in the top and bottem row
        top_cen = np.average(np.where(gray[0] == 0))
        bot_cen = np.average(np.where(gray[-1] == 0))
        #declare what value send out what data
        if top_cen - bot_center > 30: #right turns
            to_send = 255
        elif top_cen - bot_center < -20: #left turn
            to_send = 100
        else: #keep true
            to_send = 0
            
        spi = spidev.SpiDev()
        spi.open(0,0)
        spi.xfer(to_send)
#SPDR =255 , turn right
#SPDR = 100, TURN LEFT
#SPDR = 0 , DONT TURN
           
