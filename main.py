import cv2
import mediapipe as mp
import numpy as np


# ================= CAMERA =================

cap = cv2.VideoCapture(0)


# ================= MEDIAPIPE =================

mpHands = mp.solutions.hands

hands = mpHands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
)

mpDraw = mp.solutions.drawing_utils



# ================= VARIABLES =================

canvas = None

color = (255, 0, 255)

brush_size = 8
eraser_size = 50

prev_x = None
prev_y = None



# ================= TOP TOOLS =================


tools = [

    ("RED", (0,0,255)),
    ("BLUE", (255,0,0)),
    ("GREEN", (0,255,0)),
    ("PURPLE", (255,0,255)),
    ("YELLOW", (0,255,255)),
    ("ERASE", (0,0,0))

]



# ================= FUNCTIONS =================


def fingers_up(hand):

    fingers=[]


    # index, middle, ring, pinky

    tips=[8,12,16,20]


    for tip in tips:


        if hand.landmark[tip].y < hand.landmark[tip-2].y:

            fingers.append(1)


        else:

            fingers.append(0)



    return fingers






# ================= MAIN LOOP =================


while True:


    success, frame = cap.read()


    if not success:
        break



    frame = cv2.flip(frame,1)



    if canvas is None:

        canvas = np.zeros_like(frame)




    h,w,c = frame.shape





    # ================= DRAW TOP MENU =================


    box = 110



    for i,(name,col) in enumerate(tools):


        x1=i*box


        cv2.rectangle(
            frame,
            (x1,0),
            (x1+box,70),
            col,
            -1
        )



        cv2.putText(
            frame,
            name,
            (x1+10,45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,255),
            2
        )






    # ================= HAND DETECTION =================


    rgb=cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    result=hands.process(rgb)





    if result.multi_hand_landmarks:


        hand=result.multi_hand_landmarks[0]



        mpDraw.draw_landmarks(
            frame,
            hand,
            mpHands.HAND_CONNECTIONS
        )



        fingers=fingers_up(hand)



        index=hand.landmark[8]



        x=int(index.x*w)

        y=int(index.y*h)




        cv2.circle(
            frame,
            (x,y),
            12,
            color,
            -1
        )







        # ================= THREE FINGER ERASE 🤟 =================


        if (
            fingers[0]==1 and
            fingers[1]==1 and
            fingers[2]==1
        ):



            if prev_x is None:

                prev_x=x
                prev_y=y




            cv2.line(
                canvas,
                (prev_x,prev_y),
                (x,y),
                (0,0,0),
                eraser_size
            )



            prev_x=x

            prev_y=y








        # ================= TWO FINGER SELECT ✌️ =================


        elif (
            fingers[0]==1 and
            fingers[1]==1
        ):



            prev_x=None
            prev_y=None



            if y<70:


                selected=x//box



                if selected < len(tools):


                    name,col=tools[selected]


                    color=col


                    print(
                        "Selected:",
                        name
                    )










        # ================= ONE FINGER DRAW ☝️ =================


        elif fingers[0]==1:



            if prev_x is None:

                prev_x=x
                prev_y=y





            size=brush_size



            if color==(0,0,0):

                size=eraser_size






            cv2.line(
                canvas,
                (prev_x,prev_y),
                (x,y),
                color,
                size
            )




            prev_x=x

            prev_y=y








        else:


            prev_x=None

            prev_y=None







    # ================= MERGE =================


    output=cv2.add(
        frame,
        canvas
    )



    cv2.imshow(
        "AirCanvas",
        output
    )





    if cv2.waitKey(1)&0xFF==ord('q'):

        break




cap.release()

cv2.destroyAllWindows()
