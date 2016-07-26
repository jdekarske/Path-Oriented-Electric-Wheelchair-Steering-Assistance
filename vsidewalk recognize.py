import numpy as np
import cv2
# from picamera.array import PiRGBArray
# from picamera import PiCamera
import argparse
import RPi.GPIO as GPIO ## Import GPIO library
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the video")
args = vars(ap.parse_args())


cap = cv2.VideoCapture(args["video"])
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
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

#is there a better way to do this?
#signalling leds
def ledflash():
    GPIO.output(red_l,True)
    time.sleep(.1)
    GPIO.output(yellow_l2,True)
    time.sleep(.1)
    GPIO.output(yellow_l,True)
    time.sleep(.1)
    GPIO.output(green_l,True)
    time.sleep(.1)
    GPIO.output(green,True)
    time.sleep(.1)
    GPIO.output(green_r,True)
    time.sleep(.1)
    GPIO.output(yellow_r,True)
    time.sleep(.1)
    GPIO.output(yellow_r2,True)
    time.sleep(.1)
    GPIO.output(red_r,True)
    time.sleep(.1)
    GPIO.output(red_r,False)
    time.sleep(.1)
    GPIO.output(yellow_r2,False)
    time.sleep(.1)
    GPIO.output(yellow_r,False)
    time.sleep(.1)
    GPIO.output(green_r,False)
    time.sleep(.1)
    GPIO.output(green,False)
    time.sleep(.1)
    GPIO.output(green_l,False)
    time.sleep(.1)
    GPIO.output(yellow_l2,False)
    time.sleep(.1)
    GPIO.output(red_l,False)
    time.sleep(.1)
    
def ledarray(Cx, Cy):
    GPIO.output(channels,False)
    if Cx < 160:
        print('5')
        GPIO.output(red_l,True)
    elif Cx < 210:
        print('4')
        GPIO.output(yellow_l2,True)
    elif Cx < 260:
        print('3')
        GPIO.output(yellow_l,True)
    elif Cx < 300:
        print('2')
        GPIO.output(green_l,True)
    elif Cx < 340:
        print('1')
        GPIO.output(green,True)
    elif Cx < 380:
        print('2')
        GPIO.output(green_r,True)
    elif Cx < 430:
        print('3')
        GPIO.output(yellow_r,True)
    elif Cx < 480:
        print('4')
        GPIO.output(yellow_r2,True)
    else:
        print('5')
        GPIO.output(red_r,True)
        
#constants
mode = np.array([65,10,6])
totaltime = 0
loops = 0
count = 0
fps = 0.0
ledflash()
while(cap.isOpened()):
    e1 = cv2.getTickCount() #timer
    ret, frame = cap.read()

    # press esc to exit gracefully
    k = cv2.waitKey(2) & 0xFF
    if k == 27:
        break

    # load the image
    image = frame


    # blur then convert to LAB format
    #blurred = cv2.GaussianBlur(image, (5, 5), 0)
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2Lab)
     
    # establish roi in middle of image
    rows, columns, c = lab.shape
    middleroi = lab[(int(rows*.8)):rows , (int(columns*.33)):(int(columns*.66))]
    mean = cv2.mean(middleroi)
##    mean,stddev = cv2.meanStdDev(middleroi)
##    print(mean)
##    print(stddev)
##
##    #check for shadow above roi
##    shad_roi = lab[(rows*.6):(rows*.8) , (columns*.33):(columns*.66)]
##    shad_mean,shad_stddev = cv2.meanStdDev(shad_roi)
##    print(shad_mean)
##    print(shad_stddev)

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
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    ledarray(cX,cY)

    # draw the contour and center of the shape on the image
    cv2.circle(image, (cX, cY), 7, (255, 0, 255), -1)
    cv2.drawContours(image, contours, biggest, (0,255,0), 1)
    
    eroded = cv2.bitwise_and(image,image, mask= emask)
    cv2.imshow('eroded',eroded)

    #end timer
    e2 = cv2.getTickCount()
    time = (e2 - e1)/ cv2.getTickFrequency()
    totaltime += time
    loops += 1
    count += 1
    if count > 2:
        fps = loops/time
        print(fps)
        count = 0
        loops = 0
        totaltime = 0
    #display frames per sec
    
##    cv2.putText(eroded,str(int(fps)),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

###record video
##    if ret==True:
##        frame = cv2.flip(frame,0)
##
##        # write the flipped frame
##        out.write(eroded)
##    else:
##        break

##def appendtxt(var):
##    myfile.write(str(var))
##    myfile.write("\t")

#not sure how to consolidate this, testing for how to apply an auto filter. will be analyzed in excel anyway
##with open("record.txt", "a") as myfile:
##    appendtxt(area)
##    appendtxt(mean[0])
##    appendtxt(stddev[0]) #Stddev of sample~~if this is large the range should have to be bigger
##    appendtxt(mean[1])
##    appendtxt(stddev[1])
##    appendtxt(mean[2])
##    appendtxt(stddev[2])
##    appendtxt(mode[0]) #L
##    appendtxt(mode[1]) #a
##    appendtxt(mode[2]) #b
##    myfile.write("\n")

#cleanup
GPIO.cleanup()
cap.release()
out.release()
cv2.destroyAllWindows()




