from flask_bcrypt import Bcrypt
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
bcrypt = Bcrypt()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)
cur = db.cursor()

def create_user(username, password, full_name, role):
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    cur.execute("INSERT INTO Users (username, password_hash, full_name, role) VALUES (%s,%s,%s,%s)",
                (username, hashed, full_name, role))
    db.commit()

create_user("admin", "Admin@123", "Administrator", "Admin")
create_user("dr1", "Doctor@123", "Dr One", "Doctor")
create_user("nurse1", "Nurse@123", "Nurse One", "Nurse")

cur.close(); db.close()
print("Users created: admin/dr1/nurse1")
