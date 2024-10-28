import os 
import mysql.connector
from mysql.connector import Error
from models import CustomerCreate
from typing import List

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

def create_db_customer(customer_data: CustomerCreate):
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

            query = f"""
            INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)
             """

            VALUES = (customer_data.name, customer_data.email, customer_data.phone, customer_data.address)

            cursor.execute(query)

            connection.commit()

    except Error as e:
        print(f"Error while getting customers from database: {e}")

        if connection: 
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def create_db_customers_bulk(customers: List[CustomerCreate]):
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

            query = f"""
            INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)
            """

            for customer in customers:
                values = (customer.name, customer.email, customer.phone, customer.address)

                cursor.execute(query, values)

        connection.commit()

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        return True

    except Error as e:
        print(f"Error while getting customers from database: {e}")

        if connection: 
            connection.rollback()

        return False
        








