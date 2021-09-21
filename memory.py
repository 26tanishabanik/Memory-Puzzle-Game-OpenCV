import cv2
from time import sleep
import HandTrackingModule as htm
import time
import random

init_time = time.time()
counter_timeout_text = init_time+1
timer_timeout_text = init_time+1
counter_timeout = init_time+1
timer_timeout = init_time+1

def draw_text(frame, text, x, y, color=(255,0,255), thickness=4, size=3):
    if x is not None and y is not None:
        cv2.putText(frame, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)

def drawAll(img,button1=None ,buttonList = [],color_list =[] ,color = False):
    for i,button in enumerate(buttonList):
        x, y = button.pos
        w, h = button.size
        
        if color and i in [j-1 for j in color_list]:
            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 255), cv2.FILLED)
        else:
            cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
    if button1:
        button2 = button1
        x, y = button2.pos
        w, h = button2.size
        cv2.rectangle(img, button2.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, button2.text, (x + 5, y + 40),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 128), 4)
    return img
def draw(img,id):
    button = buttonList[id]
    x, y = button.pos
    w, h = button.size
    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 255), cv2.FILLED)
    return img

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
num = 1
counter = 10
for i in range(3):
    for j in range(6):
        buttonList.append(Button([150 * j + 150, 150 * i + 50], str(num)))
        num += 1
doneButton = Button([1130, 450], "Done", size = [90, 60])

init_time = time.time()
counter1_timeout_text = init_time+1
counter2_timeout_text = init_time+1
counter3_timeout_text = init_time+1
timer_timeout_text = init_time+1
counter1_timeout = init_time+1
counter2_timeout = init_time+1
counter3_timeout = init_time+1
timer_timeout = init_time+1
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=0.8)
counter1 = 3
k=0
counter2 = 50
counter3 = 10
timer = 5
actual = []

finalText = []
score = 0
k = random.randint(1, 18)
actual.append(k)
#actual = k
flag = False
add = 0
lenth = 0
start = 0
done = False
p = 0
prev = -1
n = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    _, img = detector.findHands(img)
    center_x = int(img.shape[0]/2)
    center_y = int(img.shape[0]/2)
    lmList, bboxInfo = detector.findPosition(img)
    
    if time.time() > timer_timeout_text and timer >0:
        draw_text(img, "Memorise", center_x-100, center_y, (81, 116, 233), 16, 5)
        wait2 = 10000
        while wait2 > 0:
            draw_text(img, str(timer), center_x+200, center_y+200, (81, 116, 233), 16, 5)
            wait2 -= 1
        cv2.imshow("Image", img)
        timer_timeout_text += 0.03333

    elif counter2 > 0:
        if time.time() > counter2_timeout_text and counter2 >0:
            img = drawAll(img,doneButton, buttonList)
            if p == 0:
                counter2 = counter2 + 6
            p += 1
            draw_text(img, str(counter2), 1150, 70, color = (0,255,255), thickness = 7)
            
            if time.time() > counter1_timeout_text and counter1 >0:
                if n == 0:
                    counter1 += 2.5
                n += 1
                img = draw(img, k-1)
                cv2.imshow("Image", img)
                counter1_timeout_text+=0.03333
            elif time.time() > counter3_timeout_text and counter3 >0:
                if lmList:
                    for button in buttonList:
                        x, y = button.pos
                        w, h = button.size

                        if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h:
                            cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (250, 206, 135), cv2.FILLED)
                            l, _, _ = detector.findDistance(8, 12, img)

                            
                            if l < 30:
                                
                                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                                flag = True
                                lenth += 1
                                print(lenth)
                                finalText.append(int(button.text))
                                sleep(0.15)
                        if flag and lenth == len(actual):
                            break
                    x1, y1 = doneButton.pos
                    w1, h1 = doneButton.size
                    if x1 < lmList[8][1] < x1 + w1 and y1 < lmList[8][2] < y1 + h1:
                        cv2.rectangle(img, (x1 - 5, y1 - 5), (x1 + w1 + 5, y1 + h1 + 5), (193, 182, 255), cv2.FILLED)
                        l, _, _ = detector.findDistance(8, 12, img)

                        
                        if l < 30:
                            cv2.rectangle(img, doneButton.pos, (x1 + w1, y1 + h1), (0, 255, 0), cv2.FILLED)
                            done = True
                
                    
                
                if done ==True:
                    counter2 = 0   
                
                if flag and lenth == len(actual):
                    if finalText == actual and len(finalText) == len(actual):
                        add += 1
                    else:
                        add = 0
                    sleep(0.15)
                    counter1 = 2
                    counter3 = 0
                    score += add
                    add = 0
                    k = random.randint(1, 18)
                    actual.append(k)
                    finalText = []
                    wait  = 1000
                    while wait > 0:
                        wait -= 1
                    
                    flag=False
                    lenth = 0
                draw_text(img, "Score: "+str(score), 200, 600, color = (0,255,255), thickness=7)
                cv2.imshow("Image", img)


                counter3_timeout_text+=0.03333
            if (time.time() > counter1_timeout):
                counter1-=1
                counter1_timeout+=1
            if counter1 == 0:
                counter3 = 10
            
            counter2_timeout_text+=0.03333
        if (time.time() > counter2_timeout):
            counter2-=1
            counter2_timeout+=1
        
           
    if counter2 == 0:
        wait1  = 1000
        while wait1 > 0:
            if not done:
                draw_text(img, "Time's up", center_x, center_y, color = (0,255,255), thickness = 8)
            draw_text(img, "Your Score is {}".format(score), center_x-100, center_y+100, color = (0,255,255), thickness = 8)
            wait1 -= 1
        
        cv2.imshow("Image", img)
    
    else:
        cv2.imshow("Image", img)
        
    if time.time() > timer_timeout:
        timer-=1
        timer_timeout += 1
    

    
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
    
cap.release()
cv2.destroyAllWindows()
