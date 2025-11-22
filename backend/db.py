import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

dbconfig = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", ""),
    "database": os.getenv("DB_NAME", "hospital_db"),
}

pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="hospital_pool",
    pool_size=5,
    **dbconfig
)

def get_conn():
    return pool.get_connection()
