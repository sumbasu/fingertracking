import cv2
import pyautogui
import mediapipe as mp
import time
import random

############################## DECLARE GLOBAL VARIABLES ######################

pTime = 0
dTime = 0

cIndex = 0
ndexFlag = False
cMid = 0
cRing = 0 
cPinly = 0

indexFlag = True

target_object_x = 0
target_object_y = 0
    
indexCircleAppearance = False

touched = 0

pFolded = 0
isPinkyFolded = False
    
wCam = 800
hCam = 640 
###############################################################################

def distanceCalculate(p1, p2):
    """p1 and p2 in format (x1,y1) and (x2,y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis


def drawFingerTipCircles (p,frame):
    cv2.circle(frame,center = (p[0],p[1]), radius = 10 , color = (0,255,255), thickness = 3)

def putTextonScreen (frame,fps):
    cv2.putText (frame, f'FPS : {int(fps)}', (40,70), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    cv2.putText (frame, f'Pinky Touched to Thumb: {int(cIndex)}', (40,110), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    cv2.putText (frame, f'Pinky Folded: {int(pFolded)}', (40,150), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    cv2.putText (frame, f'Index Touched Circle: {int(touched)}', (40,190), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )

#def drawCircle (int x,int y,cv2 cv, ):


def drawFoldedFingers(frame,mp_hands,hand_landmarks):

    frame_height, frame_width, _ = frame.shape
    fingers = 5
    knuckles = 4
    range_start=1
    span=4
    
    finger_points=[]

    # Build 3D array : fingers x knuckles x knuckle_coordinators i.e a 5x4x2 array
    # knuckle indices follow a predefined enumeration as defined in https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
    # 0 is represented as wrist, and hence the range_start value starts from 1 to represent first_joint of thumb, whereas 20 is the index for Pinky finger tip
    
    for x in range (fingers):
        finger_knuckles = []
        for y in range (range_start,range_start+span):
            knuckle_coordinates = []
            knuckle_coordinates.append(int (hand_landmarks.landmark[y].x * frame_width))
            knuckle_coordinates.append(int (hand_landmarks.landmark[y].y * frame_height))
            finger_knuckles.append(knuckle_coordinates)
        range_start += span
        finger_points.append(finger_knuckles)


    #Connect knuckles by line
    for j in range(fingers):
        for i in range ((knuckles-1)):
            cv2.line(frame, (finger_points[j][i][0],finger_points[j][i][1]), (finger_points[j][i+1][0],finger_points[j][i+1][1]), (24,45,255), 4)

    


def drawTrackedFingers(frame,mp_hands,hand_landmarks):

    global indexFlag
    global indexCircleAppearance
    global touched
    global cIndex
    global target_object_x
    global target_object_y

    frame_height, frame_width, _ = frame.shape

    if (indexCircleAppearance == False):
        target_object_x = random.randint(1, frame_width)
        target_object_y = random.randint(1, frame_height)
        indexCircleAppearance = True
    
    index_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
    index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            
    circle1_x = int (index_finger_x * frame_width)
    circle1_y = int (index_finger_y * frame_height)
            
    if((abs(target_object_x-circle1_x) < 8) and (abs (target_object_y - circle1_y) < 8)):
        cv2.circle(frame,center = (target_object_x,target_object_y), radius = 24 , color = (0,255,0), thickness = 25)
        indexCircleAppearance = False
        touched += 1
                
    drawFingerTipCircles ((circle1_x,circle1_y),frame)
               
    middle_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
    middle_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            
    circle1_x = int (middle_finger_x * frame_width)
    circle1_y = int (middle_finger_y * frame_height)
                
    drawFingerTipCircles ((circle1_x,circle1_y),frame)
            
    ring_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
    ring_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
            
    circle1_x = int (ring_finger_x * frame_width)
    circle1_y = int (ring_finger_y * frame_height)
                
    drawFingerTipCircles ((circle1_x,circle1_y),frame)
    
            
    pinky_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
    pinky_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
            
            
    circle1_x = int (pinky_finger_x * frame_width)
    circle1_y = int (pinky_finger_y * frame_height)
                
    drawFingerTipCircles ((circle1_x,circle1_y),frame)
            
    thumb_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
    thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            
    circle2_x = int (thumb_x * frame_width)
    circle2_y = int (thumb_y * frame_height)

    drawFingerTipCircles ((circle2_x,circle2_y),frame)

    ## calculate distance between any finger tip to thumb finger tip
                
    disI = distanceCalculate ((circle1_x,circle1_y),(circle2_x,circle2_y))
            

    #print (str(int(disI)))
            
    if ((disI < 60) and (indexFlag == False) ) :
        cIndex += 1
        indexFlag = True
            
    if ((disI > 80) and (indexFlag == True) ) :
        indexFlag = False

    drawFoldedFingers(frame,mp_hands,hand_landmarks)
    
    
#def removeCircle()

def main():
    global pTime
    global indexCircleAppearance
    global dTime
    global indexFlag
    
    print (pTime)
    cap = cv2.VideoCapture(0)

    cap.set(3,wCam)
    cap.set(4,hCam)

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,min_detection_confidence=0.5, min_tracking_confidence=0.5)

    mp_drawing = mp.solutions.drawing_utils
    
    while(True):
        ret, frame = cap.read()

        if not ret:
            break
        
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        putTextonScreen(frame,fps)
  
        cv2.circle(frame,center = (target_object_x,target_object_y), radius = 20 , color = (40,25,255), thickness = 8)

        #if more than 10 sec, then let the current circle disappea
        if ((cTime - dTime) > 10):
            dTime = cTime
            indexCircleAppearance = False
            #removeCircle(object_x,object_y,cv2,frame,radius,thickness)
            cv2.circle(frame,center = (target_object_x,target_object_y), radius = 20 , color = (40,40,40), thickness = 5) ## disappear
      
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

       
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                #mp_drawing.draw_landmarks(frame, mp_hands.HAND_CONNECTIONS)
                mp_drawing.draw_landmarks(frame, hand_landmarks,mp_hands.HAND_CONNECTIONS)
                drawTrackedFingers (frame,mp_hands,hand_landmarks)

        cv2.imshow('Hand Gesture',frame )
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
     
    cap.release()
    cv2.destroyAllWindows()
    
    
    
if __name__ == "__main__":
   main()
