import mysql.connector
from dotenv import load_dotenv 
import os 

load_dotenv()

mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user=os.getenv('MYSQL_USER'),
    passwd=os.getenv('MYSQL_PASSWORD')
)


my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE todo_db")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)