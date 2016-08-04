import RPi.GPIO as GPIO
import time
import io
import numpy as np
import cv2
import picamera
import logging

global menuv
menuv = 0
global buttonpress
buttonpress = 0

#logging setup
logging.basicConfig(format='\n%(asctime)s %(message)s', filename='/home/pi/REU/Path-Oriented-Electric-Wheelchair-Steering-Assistance/Output/data.log',level=logging.DEBUG)
logging.info('----Startup----')

#pin setup
GPIO.setmode(GPIO.BOARD)## Use board pin numbering
button   = 3
red_r    = 35
yellow_r2= 33
yellow_r = 31
green_r  = 29
green    = 23
green_l  = 21
yellow_l = 19
yellow_l2= 15
red_l    = 13
channels = [red_r, yellow_r2, yellow_r,
            green_r, green, green_l,
            yellow_l, yellow_l2, red_l]
GPIO.setup(channels, GPIO.OUT)
GPIO.setup(button, GPIO.IN)

#is there a better way to do this?
#signalling leds
def ledflash(t):
    GPIO.output(channels,False)
    GPIO.output(red_l,True)
    time.sleep(t)
    GPIO.output(yellow_l2,True)
    time.sleep(t)
    GPIO.output(yellow_l,True)
    time.sleep(t)
    GPIO.output(green_l,True)
    time.sleep(t)
    GPIO.output(green,True)
    time.sleep(t)
    GPIO.output(green_r,True)
    time.sleep(t)
    GPIO.output(yellow_r,True)
    time.sleep(t)
    GPIO.output(yellow_r2,True)
    time.sleep(t)
    GPIO.output(red_r,True)
    time.sleep(t)
    GPIO.output(red_r,False)
    time.sleep(t)
    GPIO.output(yellow_r2,False)
    time.sleep(t)
    GPIO.output(yellow_r,False)
    time.sleep(t)
    GPIO.output(green_r,False)
    time.sleep(t)
    GPIO.output(green,False)
    time.sleep(t)
    GPIO.output(green_l,False)
    time.sleep(t)
    GPIO.output(yellow_l,False)
    time.sleep(t)
    GPIO.output(yellow_l2,False)
    time.sleep(t)
    GPIO.output(red_l,False)
    time.sleep(.5)

def lederror():
    GPIO.output(channels,False)
    time.sleep(.1)
    GPIO.output(channels,True)
    time.sleep(.1)
    GPIO.output(channels,False)
    time.sleep(.1)
    GPIO.output(channels,True)
    time.sleep(.1)
    GPIO.output(channels,False)
    time.sleep(.1)
    GPIO.output(channels,True)
    time.sleep(.1)
    GPIO.output(channels,False)
    time.sleep(2)
        
    
def ledarray(Cx, Cy, center): #center at 320 make a config file for this
    GPIO.output(channels,False)
    if  (Cx < (480-center)): #160
        GPIO.output(red_l,True)
        logging.warning('Extreme left!')
    elif(Cx < (530-center)): #210
        GPIO.output(yellow_l2,True)
    elif(Cx < (580-center)): #260
        GPIO.output(yellow_l,True)
    elif(Cx < (620-center)): #300
        GPIO.output(green_l,True)
    elif(Cx < (660-center)): #340
        GPIO.output(green,True)
    elif(Cx < (700-center)): #380
        GPIO.output(green_r,True)
    elif(Cx < (750-center)): #430
        GPIO.output(yellow_r,True)
    elif(Cx < (800-center)): #480
        GPIO.output(yellow_r2,True)
    else:
        GPIO.output(red_r,True)
        logging.warning('Extreme right!')
     
def blink(color):
        GPIO.output(color,True)
        time.sleep(.1)
        GPIO.output(color,False)
        time.sleep(.1)

def main(center, record):

    #constants
    mode = np.array([65,10,6]) #inrange components for Lab. Found by doing a bunch of manual tests.
    totaltime = 0.0
    count = 0
    fps = 0.0
    resolution = (640, 480)
    totalfps = []
    global menuv #need these to communicate with the button
    global buttonpress
    
    #video recording set up
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename = '/home/pi/REU/Path-Oriented-Electric-Wheelchair-Steering-Assistance/Output/' + time.strftime('%Y%m%d_%H%M%S') + '.avi'
    out = cv2.VideoWriter(filename,fourcc, 6.0, (640,480))
    

    buttonpress = 0
    stream = io.BytesIO()
    with picamera.PiCamera(resolution=resolution) as camera:
        #camera.start_preview() #enable to see camera on screen, doesn't work with CLI
        while(buttonpress == 0): # and camera._check_camera_open()
            camera.capture(stream, format='jpeg')
            e1 = cv2.getTickCount() #timer

            # Construct a numpy array from the stream
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)

            # "Decode" the image from the array
            image = cv2.imdecode(data, 1)
            stream = io.BytesIO()

            # convert to lab format
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
             
            # establish roi in middle of image
            rows, columns, c = lab.shape
            middleroi = lab[(int(rows*.8)):rows , (int(columns*.33)):(int(columns*.66))]

            #establish range of acceptable colors
            mean = cv2.mean(middleroi)
            lowermean = np.array([mean[0]-mode[0],mean[1]-mode[1],mean[2]-mode[2]])
            uppermean = np.array([mean[0]+mode[0],mean[1]+mode[1],mean[2]+mode[2]])

            #check which part of image is in range, then filter out smaller pieces
            mask = cv2.inRange(lab, lowermean, uppermean)
            res = cv2.bitwise_and(image,image, mask= mask)
            emask1 = cv2.erode(mask,None, iterations=8)
            emask = cv2.dilate(emask1,None, iterations=12)

            #assemble better shape, select biggest area
            areas = []
            _, contours, hierarchy = cv2.findContours(emask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for i, c in enumerate(contours):
                area = cv2.contourArea(c)
                areas.append(area)
            biggest = np.argmax(areas)

            # compute the center of the contour
            M = cv2.moments(contours[biggest][:])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            ledarray(cX,cY,center)

            # draw the contour and center of the shape on the image
            cv2.circle(image, (cX, cY), 7, (255, 0, 255), -1)
#            cv2.drawContours(image, contours, biggest, (0,255,0), 1) #outlines the largest contour, not necessary
            eroded = cv2.bitwise_and(image,image, mask= emask)
#            cv2.imshow('eroded',eroded)

            #end timer, display frames per second taking the average over 10 frames
            e2 = cv2.getTickCount()
            looptime = (e2 - e1)/ cv2.getTickFrequency()
            totaltime += looptime
            count += 1
            if count > 10: 
                fps = count/totaltime
                count = 0
                totaltime = 0
                totalfps.append(fps)
                logging.info('fps: %s',fps)
#            cv2.putText(eroded,str(int(fps)),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            
        #record video
            if(record == 1):
                out.write(eroded)
    GPIO.output(channels,False)
    out.release()
    meanfps = np.mean(totalfps)
    logging.info('Average frames per second: %s', meanfps)

def calibrate():
    #constants
    mode = np.array([65,10,6])
    resolution = (640, 480)
    stream = io.BytesIO()
    with picamera.PiCamera(resolution=resolution) as camera:
        camera.capture(stream, format='jpeg')

        # Construct a numpy array from the stream
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)

        # "Decode" the image from the array, preserving colour
        image = cv2.imdecode(data, 1)
        stream = io.BytesIO()

        # blur then convert to LAB format
        #blurred = cv2.GaussianBlur(image, (5, 5), 0)
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
         
        # establish roi in middle of image
        rows, columns, c = lab.shape
        middleroi = lab[(int(rows*.8)):rows , (int(columns*.33)):(int(columns*.66))]
        mean = cv2.mean(middleroi)

        #establish range of acceptable colors
        lowermean = np.array([mean[0]-mode[0],mean[1]-mode[1],mean[2]-mode[2]])
        uppermean = np.array([mean[0]+mode[0],mean[1]+mode[1],mean[2]+mode[2]])

        #check which part of image is in range, then filter out smaller pieces
        mask = cv2.inRange(lab, lowermean, uppermean)
        res = cv2.bitwise_and(image,image, mask= mask)
        emask1 = cv2.erode(mask,None, iterations=8)
        emask = cv2.dilate(emask1,None, iterations=12)

        #assemble better shape
        areas = []
        _, contours, hierarchy = cv2.findContours(emask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i, c in enumerate(contours):
            area = cv2.contourArea(c)
            areas.append(area)
        biggest = np.argmax(areas)

        # compute the center of the contour
        M = cv2.moments(contours[biggest][:])
        cY = int(M["m01"] / M["m00"])
        cX = int(M["m10"] / M["m00"])
        if(cY > 120 & cY < 360):           
            logging.info('Calibrated!cX: %s, cY: %s', cX, cY)
            ledflash(.1)
            return cX
        else:
            logging.info('Calibration failed!cX: %s, cY: %s', cX, cY)
            lederror()
            return 0
        
def onbuttonpress(channel):
    global menuv
    global buttonhold
    global buttonpress
    time.sleep(.5)
    buttonpress = 1 # button is pressed
    if(GPIO.input(button) == 0):
        buttonhold = 1 # button is held
    else:
        menuv += 1

GPIO.add_event_detect(button, GPIO.FALLING, bouncetime=300, callback=onbuttonpress)
            
        
def menu():
    center = 320 #add to config file
    global menuv
    global buttonhold
    buttonhold = 0
    while(True):
        while(menuv == 0):
            if(buttonhold): #start
                buttonhold = 0
                logging.info('running...')
                ledflash(.1)
                main(center,0)
            blink(red_r)
        while(menuv == 1): #start, with recording
            if(buttonhold):
                buttonhold = 0
                logging.info('running (recorded)...')
                ledflash(.1)
                main(center,1)
            blink(yellow_r2)
        while(menuv == 2):#calibrate center
            if(buttonhold):
                center = 0
                while(center == 0):
                    buttonhold = 0
                    center = calibrate()
            blink(yellow_r)
        while(menuv == 3): #exit
            blink(green_r)
            if(buttonhold):
                logging.info('exiting...')
                ledflash(.01)
                ledflash(.01)
                menuv = 10
        if(buttonhold):
            break
        else:
            menuv = 0

#start stuff
ledflash(.05)
menu()

#cleanup
GPIO.cleanup()
cv2.destroyAllWindows()
logging.info('----Finish----')
    
