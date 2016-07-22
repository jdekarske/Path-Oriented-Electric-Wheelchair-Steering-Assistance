from sklearn.cluster import MiniBatchKMeans
import numpy as np
import argparse
import cv2

k = 5

image = cv2.imread("sw4")
(h, w) = image.shape[:2]
 
image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
 
# reshape into list
image = image.reshape((image.shape[0] * image.shape[1], 3))
 
# apply k-means quantization
clt = MiniBatchKMeans(n_clusters = k)
labels = clt.fit_predict(image)
quant = clt.cluster_centers_.astype("uint8")[labels]
 
# reshape the feature vectors to images
quant = quant.reshape((h, w, 3))
image = image.reshape((h, w, 3))
 
# convert from L*a*b* to RGB
quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
 
# display the images and wait for a keypress
cv2.imshow("image", np.hstack([image, quant]))
cv2.waitKey(0)
