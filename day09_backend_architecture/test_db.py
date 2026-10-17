from db import get_connection

connection = None

try:
    connection = get_connection()

    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE(), VERSION()")

    result = cursor.fetchone()

    print("MySQL connected successfully!")
    print("Database:", result[0])
    print("MySQL version:", result[1])

    cursor.close()

except Exception as error:
    print("Database connection failed:", error)

finally:
    if connection is not None and connection.is_connected():
        connection.close()