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
 
# establish roi in middle of image
rows, columns, c = lab.shape
middleroi = lab[(rows*.8):rows , (columns*.45):(columns*.55)]

# calculating object histogram
roihist = cv2.calcHist([middleroi],[1, 2], None, [256, 256], [0, 256, 0, 256] )
 
# normalize histogram and apply backprojection
cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
dst = cv2.calcBackProject([lab],[1,2],roihist,[0,256,0,256],1)
 
# Now convolute with circular disc
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cv2.filter2D(dst,-1,disc,dst)
 
# threshold and binary AND
ret,thresh = cv2.adaptiveThreshold(dst,200,ADAPTIVE_THRESH_GAUSSIAN_C,5,1.2)
thresh = cv2.merge((thresh,thresh,thresh))
res = cv2.bitwise_and(image,thresh)
 
res = np.vstack((image,thresh,res))
cv2.imwrite('res.jpg',res)

##while(1):
##    k = cv2.waitKey(2) & 0xFF
##    if k == 27:
##        break
##
##    lowermean = np.array([mean[0]-mode[0],mean[1]-mode[1],mean[2]-mode[2]])
##    uppermean = np.array([mean[0]+mode[0],mean[1]+mode[1],mean[2]+mode[2]])
##
##    mask = cv2.inRange(lab, lowermean, uppermean)
##    res = cv2.bitwise_and(image,image, mask= mask)
##    emask1 = cv2.erode(mask,None, iterations=I)
##    emask = cv2.dilate(emask1,None, iterations=I)
##    eroded = cv2.bitwise_and(image,image, mask= emask)
##
##    cv2.imshow('eroded',eroded)

cv2.destroyAllWindows()



