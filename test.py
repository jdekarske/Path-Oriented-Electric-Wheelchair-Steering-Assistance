import cv2

im = cv2.imread('sw1')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(imgray,255,0,1,11,2)
cv2.imshow('thresh', thresh)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
k = 1000
for cnt in contours:

    # first shows the original image
    im2 = im.copy()
    c = Contour(imgray,cnt)
    print c.leftmost,c.rightmost
    cv2.putText(im2,'original image',(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))       
    cv2.imshow('image',im2)
    if cv2.waitKey(k)==27:
        break
  
    im2 = im.copy()

    # Now shows original contours, approximated contours, convex hull
    cv2.drawContours(im2,[cnt],0,(0,255,0),4)
    string1 = 'green : original contour'
    cv2.putText(im2,string1,(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))
    cv2.imshow('image',im2)
    if cv2.waitKey(k)==27:
        break
  
    approx = c.approx
    cv2.drawContours(im2,[approx],0,(255,0,0),2)
    string2 = 'blue : approximated contours'
    cv2.putText(im2,string2,(20,40), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))
    cv2.imshow('image',im2)
    if cv2.waitKey(k)==27:
        break
  
    hull = c.convex_hull
    cv2.drawContours(im2,[hull],0,(0,0,255),2)
    string3 = 'red : convex hull'
    cv2.putText(im2,string3,(20,60), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))
    cv2.imshow('image',im2)
    if cv2.waitKey(k)==27:
        break

    im2 = im.copy()

    # Now mark centroid and bounding box on image
    (cx,cy) = c.centroid
    cv2.circle(im2,(int(cx),int(cy)),5,(0,255,0),-1)
    cv2.putText(im2,'green : centroid',(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))

    (x,y,w,h) = c.bounding_box
    cv2.rectangle(im2,(x,y),(x+w,y+h),(0,0,255))
    cv2.putText(im2,'red : bounding rectangle',(20,40), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))

    (center , axis, angle) = c.ellipse
    cx,cy = int(center[0]),int(center[1])
    ax1,ax2 = int(axis[0]),int(axis[1])
    orientation = int(angle)
    cv2.ellipse(im2,(cx,cy),(ax1,ax2),orientation,0,360,(255,255,255),3)
    cv2.putText(im2,'white : fitting ellipse',(20,60), cv2.FONT_HERSHEY_PLAIN, 1.0,(255,255,255))

    cv2.circle(im2,c.leftmost,5,(0,255,0),-1)
    cv2.circle(im2,c.rightmost,5,(0,255,0))
    cv2.circle(im2,c.topmost,5,(0,0,255),-1)
    cv2.circle(im2,c.bottommost,5,(0,0,255))
    cv2.imshow('image',im2)
    if cv2.waitKey(k)==27:
        break

  
    # Now shows the filled image, convex image, and distance image
    filledimage = c.filledImage
    cv2.putText(filledimage,'filledImage',(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,255)
    cv2.imshow('image',filledimage)
    if cv2.waitKey(k)==27:
        break

    conveximage = c.convexImage
    cv2.putText(conveximage,'convexImage',(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,255)
    cv2.imshow('image',conveximage)
    if cv2.waitKey(k)==27:
        break

    distance_image = c.distance_image()
    cv2.imshow('image',distance_image)
    cv2.putText(distance_image,'distance_image',(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,(255,255,255))
    if cv2.waitKey(k)==27:
        break
  
cv2.destroyAllWindows()
