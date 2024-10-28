import os 
import mysql.connector
from mysql.connector import Error
from models import OrderItemCreate
from typing import List
from fastapi import HTTPException

def db_order_item_create (order_item: OrderItemCreate):
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

            cursor.execute("SELECT id FROM orders WHERE id=%s", (order_item.order_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="The order does not exist.")

            cursor.execute("SELECT id FROM products WHERE id=%s", (order_item.product_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="The product does not exist.")
        
            query = """
            INSERT INTO order_item (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)
            """
            values = (order_item.order_id, order_item.product_id, order_item.quantity, order_item.price)  

            cursor.execute(query, values)
            connection.commit()

    except Error as e:
        print(f"Error while creating order item to database: {e}")

        if connection: 
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def db_order_item_get():
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
            SELECT i.id, i.order_id, i.product_id, i.quantity, i.price FROM order_item AS i
            """

            cursor.execute(query)

            order_item = cursor.fetchall()

    except Error as e:
        print(f"Error while getting order item from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return order_item


def create_db_order_item_bulk(orders_item: List[OrderItemCreate]):
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

            for order_item in orders_item:
                cursor.execute("SELECT id FROM orders WHERE id=%s", (order_item.order_id,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail=f"Order ID {order_item.order_id} does not exist.")

                cursor.execute("SELECT id FROM products WHERE id=%s", (order_item.product_id,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail="The product does not exist.")

                query = """
                INSERT INTO order_item (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)
                """

                for order_item in orders_item:
                    
                    values = (order_item.order_id, order_item.product_id, order_item.quantity, order_item.price)

                    cursor.execute(query, values)

        connection.commit()

    except Error as e:
        print(f"Error while creating orders item in bulk: {e}")
        if connection:
            connection.rollback()
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

    return True
    