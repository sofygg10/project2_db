import os 
import mysql.connector
from mysql.connector import Error

def db_customers_get (): 
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            query="""  
            SELECT c.id, c.name, c.email, c.phone, c.address, c.created_at FROM customers AS c
            """

            cursor.execute(query)

            customers = cursor.fetchall()

    except Error as e:
        print(f"Error while getting customers from database: {e}")

    finally:
        cursor.close()
        connection.close()
        return customers

