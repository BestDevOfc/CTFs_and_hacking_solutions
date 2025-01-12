import mysql.connector

mydb = mysql.connector.connect(
  host="HOST",
  user="USER",
  password="PASSWORD"
)

print(mydb)
