
import cv2 as cv
import numpy as np
import time

if __name__ == "__main__":

    print("hello from CV app")
    cap = cv.VideoCapture('test.mp4')
    
    
    while cap.isOpened():
        print("CV-loop")
        ret, frame = cap.read()
    
        contours_num = 10000
        rectangle_num = 10000
    
        width = int(frame.shape[1])
        height = int(frame.shape[0])
    
        target_width = 700
        target_height = int((height/width)*target_width)
    
        resized = cv.resize(frame, (target_width, target_height), interpolation=cv.INTER_AREA)
        frame = resized
    
        if not ret:
            print("Error. No frame")
            break
    
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
        edged = cv.Canny(gray, 30, 200)
        contours, hierarchy = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        cv.drawContours(frame, contours, -1, (0, 255, 0), 1) # contours[0:7]
    
     
        for cnt in contours: #[0:rectangle_num]
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    
        cv.imshow('Contours', frame)
    
        time.sleep(0.05)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
    print("buy from CV app")
