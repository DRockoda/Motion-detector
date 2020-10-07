import cv2
from datetime import datetime as dt
import pandas
import time

video=cv2.VideoCapture(0)
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=["Start","End"])

first_frame=None

video.read()
time.sleep(3.0)

while True:
    check,frame=video.read()
    status=0

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)

    threshold_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    threshold_frame=cv2.dilate(threshold_frame,None,iterations=2)

    (conts,_)=cv2.findContours(threshold_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for i in conts:
        if cv2.contourArea(i)<10000:
            continue
        status=1

        (x,y,h,w)=cv2.boundingRect(i)
        cv2.rectangle(frame,(x,y),(x+h,y+w),(255,0,0),3)
    status_list.append(status)
    status_list=status_list[-2:]
    
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(dt.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(dt.now())

    cv2.imshow("color",frame)

    key=cv2.waitKey(1)

    if key==ord('q'):
        if status==1:
            times.append(dt.now())
        break

for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

df.to_csv('times.csv')

video.release()
cv2.destroyAllWindows
