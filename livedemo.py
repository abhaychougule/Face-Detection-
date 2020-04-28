import urllib
import urllib.request
import cv2
import numpy as np
import sqlite3

url = 'http://192.168.43.1:8080/shot.jpg'
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# cam=cv2.VideoCapture(0)
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("trainner\\trainner.yml")
id = 0
font = cv2.FONT_HERSHEY_SIMPLEX


def getProfile(id):
	conn = sqlite3.connect("FaceBase.db")
	cmd = "SELECT * FROM People WHERE ID="+str(id)
	cursor = conn.execute(cmd)
	profile = None
	for row in cursor:
		profile = row
	conn.close()
	return profile


while(True):
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)

    # ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        id, conf = rec.predict(gray[y:y+h, x:x+w])
        profile = getProfile(id)
        if(profile != None):
            
            cv2.putText(img, str(profile[1]), (x, y+h), font, 2, (0, 255, 0))
        else:  
            id = "Unknown"
        cv2.imshow('Face',img)
	
        if (cv2.waitKey(1)==ord('q')):
            break


# END OF WHILEs
# cam.release()
cv2.destroyAllWindows()   
