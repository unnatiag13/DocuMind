import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
    )

    cur = conn.cursor()
    print("Database connection successful!!")
except psycopg2.OperationalError as e:
    print("Database connection failed: ",e)


