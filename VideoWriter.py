
##Startup##
import time, sys
import ps_drone													
import cv2														

drone = ps_drone.Drone()														
drone.startup()													

drone.reset()													 
while (drone.getBattery()[0]==-1):
	time.sleep(0.1)			

print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])
drone.useDemoMode(True)											

##Setup##
drone.setConfigAllID()				
drone.sdVideo()						
drone.frontCam()					
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:	time.sleep(0.0001)	
drone.startVideo()					

##Detection##
IMC = 	 drone.VideoImageCount		
stop =	 False

out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,(800,800))

while not stop:

	while drone.VideoImageCount==IMC: 
		time.sleep(0.01)

	IMC = drone.VideoImageCount
	key = drone.getKey()

	if key:		
		stop = True

	img  = drone.VideoImage	
	resize = cv2.resize(img,(800,800))
	#out.write(resize)
	cv2.imshow('Drones video',resize)
	

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	cv2.waitKey(1)				
			
cv2.destroyAllWindows() 