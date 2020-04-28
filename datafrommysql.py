import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="attendance"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM academicyear")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
