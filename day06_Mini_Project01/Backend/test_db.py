
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

try:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

    if connection.is_connected():
        print("MySQL connection successful!")
        print("Database:", os.getenv("DB_NAME"))

except mysql.connector.Error as error:
    print("MySQL connection failed.")
    print("Error:", error)

finally:
    if "connection" in locals() and connection.is_connected():
        connection.close()
