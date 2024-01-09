import cv2
import time
import imutils
import beepy

cam = cv2.VideoCapture(0)
time.sleep(1)
firstframe=None
area=300

#count = 0

while True:
    _,img=cam.read()
    text="Normal"
    grayimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gaussimg=cv2.GaussianBlur(grayimg,(21,21),0)
    if firstframe is None:
        firstframe=gaussimg
        continue
    imgdiff=cv2.absdiff(firstframe,gaussimg)
    thresh=cv2.threshold(imgdiff, 25, 255,cv2.THRESH_BINARY)[1]
    thresh=cv2.dilate(thresh, kernel=None, iterations=2)
    cont=cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont = imutils.grab_contours(cont)
    for _ in cont:
        if cv2.contourArea(_)<area:
            continue
        # (x,y,w,h) = cv2.boundingRect(_)
        # cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)


        text="Moving object detected"
        beepy.beep()
    firstframe=None
    #count+=1
    #print(count)
    #print(text)
    flip = cv2.flip(img, 1)
    cv2.putText(flip, text, (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1.5,(0,0,255), 3 )
    cv2.imshow("livefeed",flip)
    key=cv2.waitKey(1) &0xff
    if key==ord("o"):
        break
cam.release()
cv2.destroyAllWindows()
