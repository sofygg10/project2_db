import os 
import mysql.connector
from mysql.connector import Error
from models import OrderCreate
from typing import List
from fastapi import HTTPException

def db_order_create (order: OrderCreate):
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

            cursor.execute("SELECT id FROM customers WHERE id=%s", (order.customer_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="The customer does not exist.")

            else:
                query = """
                INSERT INTO orders (customer_id, total, state) VALUES (%s, %s, %s)
                """

                values = (order.customer_id, order.total, order.state)

                cursor.execute(query, values)
                connection.commit()

    except Error as e:
        print(f"Error while creating order to database: {e}")

        if connection: 
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def db_orders_get():
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
            SELECT o.customer_id, o.total, o.state FROM orders AS o
            """

            cursor.execute(query)

            products = cursor.fetchall()

    except Error as e:
        print(f"Error while getting orders from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return products


def create_db_orders_bulk(orders: List[OrderCreate]):
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

        
            for order in orders:
                cursor.execute("SELECT id FROM customers WHERE id=%s", (order.customer_id,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail=f"Customer ID {order.customer_id} does not exist.")

            query = f"""
            INSERT INTO orders (customer_id, total, state) VALUES (%s, %s, %s)
            """

            for order in orders:
                values = (order.customer_id, order.total, order.state)

                cursor.execute(query, values)

        connection.commit()

    except Error as e:
        print(f"Error while creating orders in bulk: {e}")
        if connection:
            connection.rollback()
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

    return True
