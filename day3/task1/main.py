import cv2 as cv
import numpy as np
from collections import deque
import time
import paho.mqtt.client as mqtt
import json


def draw_route(points, k, color):

    for i in range(1, len(points)):
            if points[i - 1] is None or points[i]is None:
                continue
            thickness = int(np.sqrt(64 / float(i + 1)) * k - k)
            if thickness > 0:
                cv.line(frame, points[i - 1], points[i], color, thickness)
    cv.imshow('Contours', frame)

def to_avg(points):



    list_x, list_y = [],[]

    for elem in points:
        list_x = np.append(list_x, list(elem)[0])
        list_y = np.append(list_y, list(elem)[1])
    n = 3

    if (len(points)<2 or n==0):
        return points
    sma_x = [0]*n
    sma_y = [0]*n
    sma_x.append(int(sum(list_x[0:n])/n))
    sma_y.append(int(sum(list_y[0:n])/n))

    for i in range(n+1, len(points)-1):
        sma_x.append(sma_x[i - 1])
        sma_y.append(sma_y[i - 1])

        if n != 0:
            sma_x[i] += int(list_x[i] / n)
            sma_y[i] += int(list_y[i] / n)

            sma_x[i] -= int(list_x[i - n] / n)
            sma_y[i] -= int(list_y[i - n] / n)

    result = deque(maxlen=64)

    for i in range(n, len(sma_x)):
        result.append((int(sma_x[i]), int(sma_y[i])))

    return result

if __name__ == "__main__":

    print("hello from CV app")
    points = deque(maxlen=64)
    cap = cv.VideoCapture('test2.MOV')
    client = mqtt.Client("cvSubscriber1")
    status = client.connect("localhost")
    freq_mqtt = 10
    count =0

    while cap.isOpened():
        count+=1
        print("CV-loop")
        ret, frame = cap.read()


        width = int(frame.shape[1])
        height = int(frame.shape[0])

        target_width = 300
        target_height = int((height/width)*target_width)

        resized = cv.resize(frame, (target_width, target_height), interpolation=cv.INTER_AREA)
        frame = resized

        if not ret:
            print("Error. No frame")
            break

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        edged = cv.Canny(gray, 30, 200)
        contours, hierarchy = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        rectangles = []
        rect_params = []

        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            rectangles.append([x,y,w,h])
            rect_params.append({"square": w*h, "center": (int(x + w/2), int(y + h/2)), "rectangle": [x,y,w,h] })

        rect_params = sorted(rect_params, key=lambda param: param["square"], reverse=True)
        if len(rect_params)>0:
            x, y, w, h = rect_params[0]["rectangle"]
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            points.appendleft(rect_params[0]["center"])

        draw_route(points, 2, (0, 255, 0))
        avg_points = to_avg(points)
        draw_route(to_avg(points),2,(255, 0, 0))

        if count % freq_mqtt == 0:
            x = list(points[0])[0]
            y = list(points[0])[1]
            x_avg = list(avg_points[0])[0]
            y_avg = list(avg_points[0])[1]
            msg = json.dumps({"x": x, "y": y, "x avg": x_avg, "y avg": y_avg})
            client.publish("object/route", msg)


        cv.imshow('Contours', frame)

        time.sleep(0.05)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
    print("buy from CV app")
