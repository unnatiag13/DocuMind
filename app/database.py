import psycopg2
from dotenv import load_dotenv
import os
from pgvector.psycopg2 import register_vector

load_dotenv()

try:
    conn = psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        options="-c client_encoding=UTF8"
    )
    cur = conn.cursor()
    register_vector(cur)
    print("Database connection successful!!")
except psycopg2.OperationalError as e:
    print("Database connection failed: ",e)


