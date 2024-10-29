import os 
import mysql.connector
from mysql.connector import Error
from models import CategoryCreate
from typing import List

def create_db_category(category: CategoryCreate):
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
            INSERT INTO categories (name, description) VALUES (%s, %s)
             """

            VALUES = (category.name, category.description)

            cursor.execute(query, VALUES)

            connection.commit()

    except Error as e:
        print(f"Error while creating category from database: {e}")

        if connection: 
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def db_get_categories ():

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
            SELECT c.id, c.name, c.description FROM categories AS c
            """

            cursor.execute(query)

            categories = cursor.fetchall()

    except Error as e:
        print(f"Error while getting categories from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return categories

def db_get_total_by_category ():

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
            SELECT cat.name AS category_name, SUM(oi.quantity * oi.price) AS total_sales
            FROM order_item oi
            INNER JOIN products p ON oi.product_id = p.id
            INNER JOIN categories cat ON p.category_id = cat.id
            GROUP BY cat.name;
            """

            cursor.execute(query)

            categories = cursor.fetchall()

    except Error as e:
        print(f"Error while getting categories from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return categories

def create_db_categories_bulk(categories: List[CategoryCreate]):
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
            INSERT INTO categories (name, description) VALUES (%s, %s)
            """

            for category in categories:
                values = (category.name, category.description)

                cursor.execute(query, values)

        connection.commit()

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        return True

    except Error as e:
        print(f"Error while creating categories from database: {e}")

        if connection: 
            connection.rollback()

        return False