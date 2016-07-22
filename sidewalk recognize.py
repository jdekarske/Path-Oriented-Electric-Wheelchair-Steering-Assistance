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

#empty function
def nothing(x):
    pass
if args["mode"] == 'HSV':
    colormode = np.array(['H','S','V'])
elif args["mode"] == 'Lab':
    colormode = np.array(['L','a','b'])
else:
    print("unsupported mode")

# create control window for changing parameters
cv2.namedWindow('eroded')
cv2.namedWindow('control')
cv2.createTrackbar(colormode[0],'control',0,300,nothing)
cv2.createTrackbar(colormode[1],'control',0,300,nothing)
cv2.createTrackbar(colormode[2],'control',0,300,nothing)
cv2.createTrackbar('I','control',0,20,nothing)  
 
# load the image
image = cv2.imread(args["image"])


# blur then convert to LAB format
blurred = cv2.GaussianBlur(image, (5, 5), 0)
lab = cv2.cvtColor(blurred, cv2.COLOR_RGB2HSV)


# establish roi in middle of image
rows, columns, c = lab.shape
middleroi = lab[(rows*.8):rows , (columns*.33):(columns*.66)]
mean = cv2.mean(middleroi)
print(mean)
print(cv2.mean(lab))
print(cv2.mean(image))
mode = np.array([1,1,1])
I = 1

while(1):
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    lowermean = np.array([mean[0]-mode[0],mean[1]-mode[1],mean[2]-mode[2]])
    uppermean = np.array([mean[0]+mode[0],mean[1]+mode[1],mean[2]+mode[2]])

    mask = cv2.inRange(lab, lowermean, uppermean)
    res = cv2.bitwise_and(image,image, mask= mask)
    emask1 = cv2.erode(mask,None, iterations=I)
    emask = cv2.dilate(emask1,None, iterations=I)
    eroded = cv2.bitwise_and(image,image, mask= emask)
    mode[0] = cv2.getTrackbarPos(colormode[0],'control')
    mode[1] = cv2.getTrackbarPos(colormode[1],'control')
    mode[2] = cv2.getTrackbarPos(colormode[2],'control')
    I = cv2.getTrackbarPos('I','control')

    cv2.imshow('eroded',eroded)

cv2.destroyAllWindows()
