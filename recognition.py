import cv2
import sqlite3
import numpy as np
from datetime import date
#
import mysql.connector
import datetime
#from time import gmtime, strftime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="R@ck1234",
  database="attendancenew"
)
mycursor = mydb.cursor()

#
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("trainner\\trainner.yml")
id=0
font = cv2.FONT_HERSHEY_SIMPLEX


def getProfile(id):
	conn=sqlite3.connect("FaceBase.db")
	cmd = "SELECT * FROM People WHERE ID="+str(id)
	cursor=conn.execute(cmd)
	profile=None
	for row in cursor:
		profile=row
	conn.close()
	return profile

flag=True

while(flag):
	ret, img = cam.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = faceDetect.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		id,conf=rec.predict(gray[y:y+h, x:x+w])
		profile = getProfile(id)
		if(profile!=None):
			cv2.putText(img,str(profile[1]),(x,y+h),font,2,(0, 255, 0))
			present = 1
			#time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
			time = datetime.datetime.now()
			today = date.today()
			timeslot=""
			today9am = time.replace(hour=9, minute=0, second=0, microsecond=0)
			today12pm = time.replace(hour=12, minute=0, second=0, microsecond=0)
			
			today12pm = time.replace(hour=12, minute=0, second=0, microsecond=0)
			today15pm = time.replace(hour=15, minute=0, second=0, microsecond=0)
			
			today15pm = time.replace(hour=15, minute=0, second=0, microsecond=0)
			today18pm = time.replace(hour=18, minute=0, second=0, microsecond=0)
			
			if(today9am<=time and time<=today12pm):
				timeslot="Morning"
				print("Morning")
			
			if(today12pm<=time and time<=today15pm):
				timeslot="Afternoon"
				print("Afternoon")
			
			if(today15pm<=time and time<=today18pm):
				timeslot="Evening"
				print("Evening")
			
			d1 = today.strftime("%Y-%m-%d")
			#print("d1 =", d1)
			print(profile[0])
			print(profile[1])
			
			#sql = "REPLACE INTO DeviceLogs_3_2019( `DownloadDate`, `DeviceId`, `UserId`, `LogDate`, `Direction`, `AttDirection`, `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `WorkCode`, `hrapp_syncstatus`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			#val = (time,1,profile[0],time,'','','','','','','','','','',1)
			
			selectsql="SELECT AttendanceId, StudentNumber, AttendanceTime FROM attendance WHERE CAST(AttendanceTime AS date) = '"+d1+"' AND StudentNumber='"+str(profile[0])+"' AND ((AttendanceTime BETWEEN CAST(concat(CAST(AttendanceTime AS DATE) , ' 10:00:00') AS DATETIME) AND CAST(concat(CAST(AttendanceTime AS DATE) , ' 12:00:00') AS DATETIME)) OR (AttendanceTime BETWEEN CAST(concat(CAST(AttendanceTime AS DATE) , ' 13:00:00') AS DATETIME) AND CAST(concat(CAST(AttendanceTime AS DATE) , ' 15:00:00') AS DATETIME)) OR (AttendanceTime BETWEEN CAST(concat(CAST(AttendanceTime AS DATE) , ' 16:00:00') AS DATETIME) AND CAST(concat(CAST(AttendanceTime AS DATE) , ' 18:00:00') AS DATETIME)))"
			
			#print(selectsql)
			mycursor.execute(selectsql)
			records = mycursor.fetchall()
			isRecordExists=0
			for row in records:
				isRecordExists=1
				flag=False
				
			if(isRecordExists==1):
				print("Attendance Already Marked")
				
			if(isRecordExists==0):
				sql = "INSERT INTO attendance(StudentNumber, AttendanceTime, TimeSlot) VALUES (%s, %s, %s)"
				val = (profile[0], time, timeslot)
				mycursor.execute(sql, val)

				#mydb.commit()

				#mydb.execute(sql, val)
				mydb.commit()
				#		
				print("Attendance Inserted")
		else:
			id="Unknown"
	cv2.imshow('Face',img)
	if (cv2.waitKey(1)==ord('q')):
		
		break


#END OF WHILE
cam.release()
cv2.destroyAllWindows()    
