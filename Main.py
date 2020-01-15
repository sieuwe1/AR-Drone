import cv2
import numpy as np
import imutils
import time
from collections import deque
import ps_drone


#config
Altitude = 1300

#Controller config
UpdateRate = 1
MaxMovementRatePositive = 0.020
MaxMovementRateNegative = -0.020
DivisionValueX = 14400
DivisionValueY = 9450
TargetCircleMultiplayer = 3


#variables
points = deque(maxlen=32)
counter = 0
(dX, dY) = (0, 0)
direction = ""
Run = True
Direction1 = "error"
Direction2 = "error"
raduis = 0
CircleLostCount = 0
InsideCircle = False
TargetCircleRaduis = 0

#Display variables
DisplayDx = 0.0
DisplayDy = 0.0
DisplayTreshhold = 0


font = cv2.FONT_HERSHEY_SIMPLEX

print("starting....")

drone = ps_drone.Drone()														
drone.startup()

drone.reset()													 
while (drone.getBattery()[0] == -1):  time.sleep(0.1)                         # Wait until the drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1]) # Gives a battery-status
	

#setup
drone.useDemoMode(False)
drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"])
drone.setConfigAllID()				
drone.sdVideo()						
drone.frontCam()					
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:	time.sleep(0.0001)	
drone.startVideo()

IMC = 	 drone.VideoImageCount		

time.sleep(2.0)
 
drone.takeoff()

while(Run):
    
    while drone.VideoImageCount==IMC:
        time.sleep(0.01)
        
    IMC = drone.VideoImageCount
    key = drone.getKey()
    
    if key:
        Run = False

    #if(CircleLostCount == 5):
    #    drone.land()
        
    frame = drone.VideoImage	
    
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    Greenmask = cv2.inRange(hsv, (65,60,60), (80, 255,255))
    Greenmask = cv2.erode(Greenmask, None, iterations=2)
    Greenmask = cv2.dilate(Greenmask, None, iterations=2)
    
    FoundedContours = cv2.findContours(Greenmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    FoundedContours = imutils.grab_contours(FoundedContours)
    center = None

    if len(FoundedContours) > 0:
        Circle = max(FoundedContours, key=cv2.contourArea)
        ((x,y),raduis) = cv2.minEnclosingCircle(Circle)
        Middle = cv2.moments(Circle)

        center = (int(Middle["m10"] / Middle["m00"]), int(Middle["m01"] / Middle["m00"]))

        if raduis > 10:
            cv2.circle(frame,(int (x),int (y)),int(raduis),(0,0,255),2)
            TargetCircleRaduis = raduis * TargetCircleMultiplayer
            cv2.circle(frame,(int (x),int (y)),int(TargetCircleRaduis),(255,255,0),2)
            cv2.circle(frame,center,5,(0,255,255),-1)
            points.appendleft(center)
        else:
            cv2.putText(frame,"Error no circel Found",(10,700), font, 1,(255,255,255),2,cv2.LINE_AA)
            #CircleLostCount+= 1

    else:
        cv2.putText(frame,"Error no circel Found",(10,700), font, 1,(255,255,255),2,cv2.LINE_AA)
        #CircleLostCount+= 1

    DxCount = 0.0
    DyCount = 0.0

    for i in np.arange(1, len(points)):
        if points[i - 1] is None or points[i] is None:
            continue
        #check if 400,400 is in surface of circle ((x,y),raduis) if case then no need to do calculations

        if counter >= 10 and i == 1:
            
            print("Y points: " + str(points[i][1]))

            DxCount = float(points[i][0])-320.0 
            DyCount = 170 - float(points[i][1])

            cv2.line(frame, points[i - 1], (320,170), (0, 0, 255), 5)

            #cv2.putText(frame,str(DxCount),(10,100), font, 1,(255,0,0),2,cv2.LINE_AA)
            #cv2.putText(frame,str(DyCount),(10,150), font, 1,(255,0,0),2,cv2.LINE_AA)

            if(DxCount < 0):
                Direction1 = "Need to go Left"

            if(DxCount > 0):
                Direction1 = "Need to go Right"

            if(DyCount < 0):
                Direction2 = "Need to go Up"

            if(DyCount > 0):
                Direction2 = "Need to go Down"

            if (int(points[i][0]) - 320)**2 + (int(points[i][1]) - 170)**2 < (TargetCircleRaduis)**2:
                InsideCircle = True
            else:
                
                InsideCircle = False

    cv2.putText(frame,"Inside circel" + str(InsideCircle),(10,120), font, 1,(255,0,0),2,cv2.LINE_AA)

    

    CurrentAltitude = drone.NavData["altitude"][3]
    
    if(counter % UpdateRate) == 0:

        DisplayDx = DxCount
        DisplayDy = DyCount
        DisplayTreshhold = CurrentAltitude - Altitude

        Xmovement = DxCount / DivisionValueX #6400
        Ymovement = (DyCount / DivisionValueY) #4200

        if Xmovement > MaxMovementRatePositive:
            Xmovement = MaxMovementRatePositive
        elif Xmovement < MaxMovementRateNegative:
            Xmovement = MaxMovementRateNegative
        if Ymovement > MaxMovementRatePositive:
            Ymovement = MaxMovementRatePositive
        elif Ymovement < MaxMovementRateNegative:
            Ymovement = MaxMovementRateNegative

        print("X: " + str(Xmovement) + "      Y:" + str(Ymovement) )  

        AltitudeCommand = 0.0

        if (CurrentAltitude - Altitude) > 80:
            AltitudeCommand = -0.2
        elif (CurrentAltitude - Altitude) < -80:
            AltitudeCommand = 0.2
        else:
            AltitudeCommand = 0.0
        

        if(InsideCircle == False):
            drone.move(Xmovement, Ymovement, AltitudeCommand, 0)

        else:
            if(AltitudeCommand != 0.0):
                drone.move(0, 0, AltitudeCommand, 0)
            else:
                drone.stop()


        #time.sleep((DxCount / 320.0 + DyCount / 210.0) / 2.0)

    cv2.putText(frame,Direction1,(10,30), font, 1,(255,0,0),2,cv2.LINE_AA)
    cv2.putText(frame,Direction2,(10,60), font, 1,(255,0,0),2,cv2.LINE_AA)
    cv2.putText(frame,"Altitude Treshhold: " + str(DisplayTreshhold),(10,90), font, 1,(255,0,0),2,cv2.LINE_AA)
   

    cv2.circle(frame,(320,170),10,(255,0,0),-1)

    cv2.imshow("Detected",frame)
    counter += 1
 
    if cv2.waitKey(25) & 0xFF == ord('q'):
	break

cv2.destroyAllWindows()


    
