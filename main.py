import cv2
from cvzone.HandTrackingModule import HandDetector
import time

class Key:

    def __init__(self,char,start,end):
        self.char = char
        self.start = start
        self.end = end
    
    def render(self,img):
        img = cv2.rectangle(img,self.start,self.end,(0,255,0),cv2.FILLED)
        img = cv2.putText(img,self.char,(self.start[0] + 15,self.start[1] + 35),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
        return img


def render_all(keys,img):
    
    for key in keys:
        key.render(img)

def capture(hand,img):

    char = ""
    lm_list = hand["lmList"]
    if lm_list:
        for key in keys:
            if key.start[0] < lm_list[8][0] < key.end[0] and key.start[1] < lm_list[8][1] < key.end[1]:
                img = cv2.rectangle(img,key.start,key.end,(0,150,0),cv2.FILLED)
                img = cv2.putText(img,key.char,(key.start[0] + 15,key.start[1] + 35),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
                length,info = detector.findDistance(lm_list[8][:2],lm_list[12][:2])
                if length < 50:
                    img = cv2.rectangle(img,key.start,key.end,(150,150,0),cv2.FILLED)
                    img = cv2.putText(img,key.char,(key.start[0] + 15,key.start[1] + 35),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
                    char = key.char
                    time.sleep(0.3)
    return img,char

chars = [
    ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R"],
    ["S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0"],
]

keys = []
for i,row in enumerate(chars):
    for j,char in enumerate(row):
        keys.append(Key(char,(10 + 70 * j,60 + 70 * i),(60 + 70 * j,110 + 70 * i)))

vid = cv2.VideoCapture(0)
vid.set(3,1280)
vid.set(4,720)

detector = HandDetector(maxHands = 2,detectionCon = 0.8)

output = ""
while True:
    success,img = vid.read()
    img = cv2.flip(img,1)
    hands = detector.findHands(img,draw = False)
    render_all(keys,img)
    if hands:
        if len(hands) > 0:
            img,char = capture(hands[0],img)
            output += char
        if len(hands) > 1:
            img,char = capture(hands[1],img)
            output += char
    img = cv2.rectangle(img,(10,10),(1270,50),(150,150,0),cv2.FILLED)
    img = cv2.putText(img,output,(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
    cv2.imshow("img",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()