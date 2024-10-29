import os 
import mysql.connector
from mysql.connector import Error
from models import ShippingStateCreate
from typing import List
from fastapi import HTTPException

def db_shipping_state_create(shipping_state: ShippingStateCreate):
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT id FROM orders WHERE id=%s", (shipping_state.order_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="The order does not exist.")
            else:
                query = """
                INSERT INTO shipping_status (order_id, status, tracking_number) VALUES (%s, %s, %s)
                """

                values = (shipping_state.order_id, shipping_state.status, shipping_state.tracking_number)

                cursor.execute(query, values)
                connection.commit()

    except Error as e:
        print(f"Error while creating shipping state to database: {e}")

        if connection: 
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def db_shipping_status_get():
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
            SELECT s.id, s.order_id, s.status, s.tracking_number FROM shipping_status AS s
            """

            cursor.execute(query)

            products = cursor.fetchall()

    except Error as e:
        print(f"Error while getting shipping status from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return products

def db_orders_shipping_status():
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
            SELECT o.id AS order_id, o.total AS order_total, s.status AS shipping_status
            FROM orders o
            LEFT JOIN shipping_status s ON o.id = s.order_id;
            """

            cursor.execute(query)

            products = cursor.fetchall()

    except Error as e:
        print(f"Error while getting shipping status from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return products