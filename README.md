# AR-Drone
Code for making a AR drone 2.0 fly above a red circle all by itself using openCV and python 2.7

[![Demo](https://img.youtube.com/vi/Vgv0OpEXAWI/0.jpg)](https://www.youtube.com/watch?v=Vgv0OpEXAWI)

# Installation
1. Install Python 2.7
2. Install OpenCV 3 for python 2.7
3. Install PS-Drone 

# How to run?
1. Connect AR drone to your computer using the AR drone WiFi network
2. Run Main.py with python2.7 
3. Enjoy!

**NOTE: I modded the AR-Drone by getting the front camera of the AR-Drone and taped it to the bottom center of the drone. If you do it correctly the existing flex cable is just long enough! This is because the normal AR-Drone bottom camera is very low resolution. If you want to run this code also make sure to do this mod!**

**NOTE 2: You might have to help the drone a little bit at takeoff. This is because the AR-Drone drifts a lot at takeoff and because of that it could lose sight of the Circle. Just push the drone into the direction of the circle when it takes off.**

# Files
1. tag.png This is the circle which the drone detect. Print this out with a diameter of about 35cm
2. Main.py the main program which will make the drone center above the tag.
3. VideoWrite.py A simple program which writes the video stream from the AR Drone to a local .avi video.

# For questions feel free to contact me using the Issues tab in Github!
