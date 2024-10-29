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

def db_customers_get_orders (customer_id): 
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
                        SELECT 
                c.id AS customer_id,
                c.name AS customer_name,
                c.email AS customer_email,
                o.id AS order_id,
                o.total AS order_total,
                o.created_at AS order_date,
                o.state AS order_status,
                oi.id AS order_item_id,
                p.name AS product_name,
                oi.quantity AS product_quantity,
                oi.price AS product_price
            FROM 
                customers c
            JOIN 
                orders o ON c.id = o.customer_id
            JOIN 
                order_item oi ON o.id = oi.order_id
            JOIN 
                products p ON oi.product_id = p.id
            WHERE 
                c.id = %s;

            """

            cursor.execute(query, (customer_id,))

            customers = cursor.fetchall()

    except Error as e:
        print(f"Error while getting customers from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return customers

def db_highest_per_customer_get (): 
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
            SELECT o.customer_id, MAX(o.total) AS highest_order_total
            FROM orders o
            GROUP BY o.customer_id;
            """

            cursor.execute(query)

            customers = cursor.fetchall()

    except Error as e:
        print(f"Error while getting customers from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return customers

def db_without_orders_get (): 
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
            SELECT c.id AS customer_id, c.name AS customer_name
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            WHERE o.id IS NULL;
            """

            cursor.execute(query)

            customers = cursor.fetchall()

    except Error as e:
        print(f"Error while getting customers from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return customers

def db_customers_highest_order (): 
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
            SELECT c.id AS customer_id, c.name AS customer_name, o.id AS order_id, o.total AS order_total
            FROM customers c
            INNER JOIN orders o ON c.id = o.customer_id
            WHERE o.total = (SELECT MAX(total) FROM orders);
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

            cursor.execute(query, VALUES)

            connection.commit()

    except Error as e:
        print(f"Error while creating customers from database: {e}")

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
        








