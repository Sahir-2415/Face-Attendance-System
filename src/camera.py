import cv2
import numpy as np
cap=cv2.VideoCapture(0)
# faces=face_cascade.detectMultiScale(gray);
while(True):
    if not cap.isOpened():
        break
    ret,frame=cap.read()
    if not ret:
        break
    print(type(frame))
    print(frame.shape)
    
    cv2.imshow("Camera",frame)
    if cv2.waitKey(1)==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()