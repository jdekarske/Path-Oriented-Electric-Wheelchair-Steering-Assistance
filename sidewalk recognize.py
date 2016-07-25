import numpy as np
import cv2
# from picamera.array import PiRGBArray
# from picamera import PiCamera
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
ap.add_argument("-m", "--mode", help = "HSV or Lab mode")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])


# blur then convert to LAB format
blurred = cv2.GaussianBlur(image, (5, 5), 0)

#check mode argument
if args["mode"] == 'HSV':
    colormode = np.array(['H','S','V'])
    lab = cv2.cvtColor(blurred, cv2.COLOR_RGB2HSV)
elif args["mode"] == 'Lab':
    colormode = np.array(['L','a','b'])
    lab = cv2.cvtColor(blurred, cv2.COLOR_RGB2Lab)
else:
    print("unsupported mode")

#empty function
def nothing(x):
    cv2.destroyWindow('eroded')

# create control window for changing parameters
cv2.namedWindow('control')
cv2.createTrackbar(colormode[0],'control',65,300,nothing)
cv2.createTrackbar(colormode[1],'control',5,300,nothing)
cv2.createTrackbar(colormode[2],'control',11,300,nothing)
cv2.createTrackbar('I','control',10,20,nothing)  
 
# establish roi in middle of image
rows, columns, c = lab.shape
middleroi = lab[(int(rows*.8)):rows , (int(columns*.33)):(int(columns*.66))]
mean,stddev = cv2.meanStdDev(middleroi)
##print(mean)
##print(stddev)

#check for shadow above roi
##shad_roi = lab[(rows*.6):(rows*.8) , (columns*.33):(columns*.66)]
##shad_mean,shad_stddev = cv2.meanStdDev(shad_roi)
##print(shad_mean)
##print(shad_stddev)

mode = np.array([65,5,11])
I = 10
area = np.array(np.zeros(1000)) #this should be better

while(1):
    k = cv2.waitKey(2) & 0xFF
    if k == 27:
        break

    lowermean = np.array([mean[0]-mode[0],mean[1]-mode[1],mean[2]-mode[2]])
    uppermean = np.array([mean[0]+mode[0],mean[1]+mode[1],mean[2]+mode[2]])

    #check which part of image is in range, then filter out smaller pieces
    mask = cv2.inRange(lab, lowermean, uppermean)
    res = cv2.bitwise_and(image,image, mask= mask)
    emask1 = cv2.erode(mask,None, iterations=9)
    emask = cv2.dilate(emask1,None, iterations=11)

    #assemble better shape
    areas = []
    _, contours, hierarchy = cv2.findContours(emask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        areas.append(area)
    biggest = np.argmax(areas)

    cv2.drawContours(image, contours, biggest, (0,255,0), 1)
    
    eroded = cv2.bitwise_and(image,image, mask= emask)

    #get trackbar value
    mode[0] = cv2.getTrackbarPos(colormode[0],'control')
    mode[1] = cv2.getTrackbarPos(colormode[1],'control')
    mode[2] = cv2.getTrackbarPos(colormode[2],'control')
    I = cv2.getTrackbarPos('I','control')
    cv2.imshow('eroded',eroded)


def appendtxt(var):
    myfile.write(str(var))
    myfile.write("\t")

#not sure how to consolidate this, testing for how to apply an auto filter. will be analyzed in excel anyway
with open("record.txt", "a") as myfile:
    appendtxt(area)
##    appendtxt(mean[0])
##    appendtxt(stddev[0]) #Stddev of sample~~if this is large the range should have to be bigger
##    appendtxt(mean[1])
##    appendtxt(stddev[1])
##    appendtxt(mean[2])
##    appendtxt(stddev[2])
##    appendtxt(mode[0]) #L
##    appendtxt(mode[1]) #a
##    appendtxt(mode[2]) #b
    myfile.write("\n")
cv2.destroyAllWindows()


