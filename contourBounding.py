import numpy as np
import cv2
import time
import wiringpi
 
# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()
  
# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
   
# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
    
# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)
     
delay_period = 0.01

xPos = 0
yPos = 0
x = 0
y = 0
w = 0
h = 0
cap = cv2.VideoCapture(0)
pulse = 150
while(True):
    #Start FPS timer at beginning of loop
    timer = cv2.getTickCount()
    # Capture frame-by-frame
    ret, frame = cap.read()
    try:
        height, width = frame.shape[:2]
        xPos = width/2
        yPos = height/2
        frame = cv2.resize(frame, (int(width/1), int(height/1)), interpolation = cv2.INTER_AREA)

    # Our operations on the frame come here
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.inRange(frame, (30, 0.0, 0.0), (255, 32.037, 66.67232))
        im2, contours, hi = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            contours = list(filter(lambda x: cv2.contourArea(x) > 1000, contours))	
        if len(contours) != 0:
            cv2.drawContours(frame, contours, -1, (255, 255, 0), 1)
            c = max(contours, key = cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            xPos = x + w/2
            yPos = y + h/2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
    #Displays frame
        print(xPos, yPos)
        cv2.circle(frame, (int(x+w/2), int(y+h/2)), (int(min([w, h])/8)), (100, 100, 100), -1)
        cv2.putText(frame, "X : " + str(xPos), (50,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        cv2.putText(frame, "Y : " + str(yPos), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        cv2.imshow('peephole', frame)
        pulse = int((((yPos - 0) * 160) / (height)) + 70)
        wiringpi.pwmWrite(18,pulse) 
    except AttributeError:
        print("kek")
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
