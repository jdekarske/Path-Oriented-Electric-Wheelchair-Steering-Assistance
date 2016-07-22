import cv2
import numpy as np
from matplotlib import pyplot as plt
 
img = cv2.imread('sw2')
hsv = cv2.cvtColor(img,cv2.COLOR_RGB2Lab)
hist = cv2.calcHist( [hsv], [1, 2], None, [256, 256], [0, 256, 0, 256] )


plt.imshow(hist,interpolation = 'nearest')
plt.show()
