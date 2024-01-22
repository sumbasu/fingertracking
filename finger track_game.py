import cv2
import pyautogui
import mediapipe as mp
import time
import random

def distanceCalculate(p1, p2):
    """p1 and p2 in format (x1,y1) and (x2,y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis

#def drawCircle (int x,int y,cv2 cv, ):
    
    
#def removeCircle()
    
    

wCam = 800
hCam = 640 
cap = cv2.VideoCapture(0)

cap.set(3,wCam)
cap.set(4,hCam)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

pTime = 0
dTime = 0

cIndex = 0
indexFlag = False
cMid = 0
cRing = 0 
cPinly = 0

object_x = 0;
object_y = 0;
indexCircleAppearance = False

touched = 0

while True:
    ret, frame = cap.read()
    
    frame_height, frame_width, _ = frame.shape 
    #frame_height, frame_width = 800,640
    
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    
    
    if (indexCircleAppearance == False):
        object_x = random.randint(1, frame_width)
        object_y = random.randint(1, frame_height)
        indexCircleAppearance = True
    
   # drawCircle(object_x,object_y,cv2,frame,radius,thickness)
   
    cv2.circle(frame,center = (object_x,object_y), radius = 20 , color = (40,25,255), thickness = 8)
    
    if ((cTime - dTime) > 10):
        dTime = cTime
        indexCircleAppearance = False
        #removeCircle(object_x,object_y,cv2,frame,radius,thickness)
        cv2.circle(frame,center = (object_x,object_y), radius = 20 , color = (40,40,40), thickness = 5) ## disappear
    
    
    
    cv2.putText (frame, f'FPS : {int(fps)}', (40,70), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    
    cv2.putText (frame, f'Pinky Touched to Thumb: {int(cIndex)}', (40,110), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    
    cv2.putText (frame, f'Index Touched Circle: {int(touched)}', (40,150), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            #mp_drawing.draw_landmarks(frame, hand_landmarks)

            index_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            
            circle1_x = int (index_finger_x * frame_width)
            circle1_y = int (index_finger_y * frame_height)
            
            if((abs(object_x-circle1_x) < 8) and (abs (object_y - circle1_y) < 8)):
                cv2.circle(frame,center = (object_x,object_y), radius = 24 , color = (0,255,0), thickness = 15)
                cv2.circle(frame,center = (object_x,object_y), radius = 26 , color = (0,255,0), thickness = 16)
                indexCircleAppearance = False
                touched += 1
                
                
            cv2.circle(frame,center = (circle1_x,circle1_y), radius = 10 , color = (0,255,255), thickness = 3)
            
            #print (mp_hands.HandLandmark)
            middle_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
            middle_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            
            circle1_x = int (middle_finger_x * frame_width)
            circle1_y = int (middle_finger_y * frame_height)
                
            cv2.circle(frame,center = (circle1_x,circle1_y), radius = 10 , color = (0,255,255), thickness = 3)
            
            ring_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
            ring_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
            
            circle1_x = int (ring_finger_x * frame_width)
            circle1_y = int (ring_finger_y * frame_height)
                
            cv2.circle(frame,center = (circle1_x,circle1_y), radius = 10 , color = (0,255,255), thickness = 3)
            
            pinky_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
            pinky_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
            
            
            circle1_x = int (pinky_finger_x * frame_width)
            circle1_y = int (pinky_finger_y * frame_height)
                
            cv2.circle(frame,center = (circle1_x,circle1_y), radius = 10 , color = (0,255,255), thickness = 3)
            
            thumb_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            
            circle2_x = int (thumb_x * frame_width)
            circle2_y = int (thumb_y * frame_height)

            cv2.circle(frame,center = (circle2_x,circle2_y), radius = 10 , color = (255,255,0), thickness = 3)
            
            #cv2.line (frame,(circle1_x,circle1_y),(circle2_x,circle2_y), (255,0,0),4)
            
            disI = distanceCalculate ((circle1_x,circle1_y),(circle2_x,circle2_y))
            
            print (str(int(disI)))
            
            if ((disI < 60) and (indexFlag == False) ) :
                cIndex += 1
                indexFlag = True
            
            if ((disI > 80) and (indexFlag == True) ) :
                indexFlag = False
            #

            #cv2.circle(frame,center = (thumb_x,thumb_y))
            
            # if index_finger_y < thumb_y:
            #     hand_gesture = 'pointing up'
                
            # elif index_finger_y > thumb_y:
            #     hand_gesture = 'pointing down'
            # else:
            #     hand_gesture = 'other'

            # if hand_gesture == 'pointing up':
            #     pyautogui.press('volumeup')
            # elif hand_gesture == 'pointing down':
            #     pyautogui.press('volumedown')

    cv2.imshow('Hand Gesture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
