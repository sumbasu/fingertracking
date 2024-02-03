import cv2
import pyautogui
import mediapipe as mp
import time
import random

############################## DECLARE GLOBAL VARIABLES ######################

pTime = 0
dTime = 0

fingers = 5

touchCount = [0 for col in range(fingers)] 
fingerFoldCount = [0 for col in range(fingers)] 
newIndexFlag=[True for col in range(fingers)] 

indexFlag = True

target_object_x = 0
target_object_y = 0
    
indexCircleAppearance = False

touched = 0

pFolded = 0
isPinkyFolded = False
    
wCam = 800
hCam = 640

fingers = 5
knuckles = 4
range_start=1
span=4
    
finger_points=[]
finger_tip_circles=[]
finger_tip_distance=[]
#finger_knuckles=[]
#knuckle_coordinates=[]
###############################################################################

def distanceCalculate(p1, p2):
    """p1 and p2 in format (x1,y1) and (x2,y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis


def drawFingerTipCircles (p,frame):
    cv2.circle(frame,center = (p[0],p[1]), radius = 10 , color = (0,255,255), thickness = 3)

def putTextonScreen (frame,fps):
    cv2.putText (frame, f'FPS : {int(fps)}', (40,70), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    cv2.putText (frame, f'Pinky Touched to Thumb: {int(touchCount[4])}', (40,110), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    cv2.putText (frame, f'Ring Touched to Thumb: {int(touchCount[3])}', (40,150), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    cv2.putText (frame, f'Middle Touched to Thumb: {int(touchCount[2])}', (40,190), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    cv2.putText (frame, f'Index Touched to Thumb: {int(touchCount[1])}', (40,230), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    #cv2.putText (frame, f'Pinky Folded: {int(pFolded)}', (40,270), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )
    cv2.putText (frame, f'Index Touched Circle: {int(touched)}', (40,310), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3 )

#def drawCircle (int x,int y,cv2 cv, ):


#def drawFoldedFingers(frame,mp_hands,hand_landmarks):
def drawFoldedFingers(frame):
    frame_height, frame_width, _ = frame.shape


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
    global fingers
    global knuckles
    global range_start
    global span
    global finger_points
    global finger_tip_circles
    global finger_tip_distance
    global newIndexFlag
    global touchCount
  
    

    frame_height, frame_width, _ = frame.shape

    if (indexCircleAppearance == False):
        target_object_x = random.randint(1, frame_width)
        target_object_y = random.randint(1, frame_height)
        indexCircleAppearance = True

    for x in range (fingers):
        finger_knuckles = []
        for y in range (range_start, range_start+ span):
            knuckle_coordinates = []
            knuckle_coordinates.append(int (hand_landmarks.landmark[y].x * frame_width))
            knuckle_coordinates.append(int (hand_landmarks.landmark[y].y * frame_height))
            finger_knuckles.append(knuckle_coordinates)
        range_start +=  span
        finger_points.append(finger_knuckles)

    for j in range(fingers):
       circle_coordinates=[]
       circle_coordinates.append(int (finger_points[j][3][0])) # x coordinate of the tip of the specific finger
       circle_coordinates.append(int (finger_points[j][3][1])) # y coordinate of the tip of the specific finger
    
       drawFingerTipCircles ((circle_coordinates[0],circle_coordinates[1]),frame) # draw small circle around tip of the finger
       
       finger_tip_circles.append(circle_coordinates) # append x, y coordinates of finger tip in fingertip array
       
       if ( j == 1 ): ## for index finger
           if((abs(target_object_x-circle_coordinates[0]) < 8) and (abs (target_object_y - circle_coordinates[1]) < 8)):
               cv2.circle(frame,center = (target_object_x,target_object_y), radius = 24 , color = (0,255,0), thickness = 25)
               indexCircleAppearance = False
               touched += 1
            

    for j in range(fingers):
        circle1_x = finger_tip_circles[j][0]
        circle1_y = finger_tip_circles[j][1]
        circle2_x = finger_tip_circles[0][0]  ## this is thumb's tip's x coordinate
        circle2_y = finger_tip_circles[0][1] ## this is thumb's tip's y coordinate 
        finger_tip_distance.append(distanceCalculate ((circle1_x,circle1_y),(circle2_x,circle2_y)))
    

    ## calculate distance between any finger tip to thumb finger tip

 
            
    disI = finger_tip_distance[4]
    for j in range (fingers):
        disI = finger_tip_distance[j]
        if ((disI < 60) and (newIndexFlag[j] == False) ) :
            touchCount[j] += 1
            newIndexFlag[j] = True
        if ((disI > 80) and (newIndexFlag[j] == True) ) :
            newIndexFlag[j] = False

    #drawFoldedFingers(frame,mp_hands,hand_landmark)
    drawFoldedFingers(frame)

    
    finger_points.clear()
    finger_tip_circles.clear()
    finger_tip_distance.clear()
    range_start = 1
    
    
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
