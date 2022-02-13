import cv2
import time
import  numpy as np
import handtrackingmodule as htm
import math
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

########################

wCam, hCam = 1280, 720


cap = cv2.VideoCapture(0)
"""
cap.set(3, wCam)
cap.set(4,hCam)
"""

pTime = 0

detector = htm.handDetector(max_hands=1, detection_confidence=0.7, track_confidence=0.7)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()

volRange = volume.GetVolumeRange()



minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volbar = 400
volpercent = 0
area = 0

print(volume.GetVolumeRange())




while True:
    
    success, img = cap.read()
    
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img, draw=False, bbox=True)
    
    if len(lmlist) != 0:
        
        wB, hB = bbox[2]-bbox[0], bbox[3]-bbox[1]
        area = wB * hB //100
        
        #print(area)
        #print(lmlist[4], lmlist[8])
        
        if 250<area<1200:
        
            #print("yes")
            
            length, img, lineInfo = detector.findDistance(4,8,img)
            
            #print(length)
            
                        
            vol = np.interp(length,[70,200],[minVol,maxVol])
            volbar = np.interp(length,[50,200],[400,150])
            volpercent = np.interp(length,[50,200],[0,100])
            
            
            smoothness = 5 
            volpercent = smoothness * round(volpercent/smoothness)
            
            fingers = detector.fingersUp()
            
            print(fingers)
            
            if not fingers[3]:
                volume.SetMasterVolumeLevelScalar(volpercent/100, None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                

            #print(vol)
            
            
            #volume.SetMasterVolumeLevel(vol, None)
            
            
            
            #print(length)
            
            #hand range 50-230
            #vol range -65 - 0



            
    cv2.rectangle(img, (50,150), (85,400),(0,255,0), 3)
    cv2.rectangle(img, (50,int(volbar)), (85,400),(0,255,0), cv2.FILLED)
    cv2.putText(img, str(round(volpercent)), (50,450), cv2.FONT_HERSHEY_PLAIN, 3,(0,255,0),3)
            
        
    
    
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime    
    
    cv2.putText(img, str(round(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3,(0,255,0),3) #display fps
    
    cv2.imshow("image", img)
    cv2.waitKey(1)
