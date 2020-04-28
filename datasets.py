import sys
import cv2
import numpy as np
import sqlite3

import mysql.connector

from time import gmtime, strftime
time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="attendancenew"
)
mycursor = mydb.cursor()

cap=cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def insertOrUpdate(Id, Name1):
	conn=sqlite3.connect("FaceBase.db")
	#print("here", id, name)
	cmd="SELECT * FROM People where ID="+str(Id)
	cursor=conn.execute(cmd)
	isRecordExists=0
	for row in cursor:
		isRecordExists=1
	if(isRecordExists==1):
		cmd="UPDATE People SET Name='"+str(name)+"' WHERE ID="+str(Id)
		#print(cmd)
	else:
		cmd="INSERT INTO People(ID,Name) Values("+str(Id)+",'"+str(Name1)+"')"
		#
		sql = "INSERT INTO Student(StudentNumber, StudentName) VALUES(%s, %s)"
		#val = (time,1,profile[0],time,'','','','','','','','','','',1)
		val =(str(Id), str(Name1))
		
		#
		#print(cmd)
	#	
	mycursor.execute(sql, val)
	mydb.commit()	
	#
	conn.execute(cmd)
	conn.commit()
	conn.close()
	#fun close


id = input("enter user id =  ")
name = input("enter name =  ")
mycursor = mydb.cursor()

#sql = "INSERT INTO students (id, name) VALUES (%s, %s)"
#val = (id, name)
#mycursor.execute(sql, val)
#mydb.commit()


insertOrUpdate(id,name)
num=0

while(True):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        num = num + 1
        cv2.imwrite("dataSet/User."+str(id)+"."+str(num)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.waitKey(100)
    cv2.imshow('frame',img)
    cv2.waitKey(100)

    if(num>50):
        cap.release()
        cv2.destroyAllWindows()  
        break

  
