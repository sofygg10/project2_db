import os 
import mysql.connector
from mysql.connector import Error
from models import ProductCreate
from typing import List
from fastapi import HTTPException

def db_product_create(product: ProductCreate):
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

            cursor.execute("SELECT id FROM categories WHERE id=%s", (product.category_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="The category does not exist.")
            else:
                query = """
                INSERT INTO products (name, description, price, stock, category_id) VALUES (%s, %s, %s, %s, %s)
                """

                values = (product.name, product.description, product.price, product.stock, product.category_id)

                cursor.execute(query, values)
                connection.commit()

    except Error as e:
        print(f"Error while creating product to database: {e}")

        if connection: 
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def db_products_get():
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
            SELECT p.id, p.name, p.description, p.price, p.stock, p.category_id FROM products AS p
            """

            cursor.execute(query)

            products = cursor.fetchall()

    except Error as e:
        print(f"Error while getting products from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return products

def db_products_categories_get():
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
            SELECT p.id AS product_id, p.name AS product_name, c.name AS category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id;
            """

            cursor.execute(query)

            products = cursor.fetchall()

    except Error as e:
        print(f"Error while getting products from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return products

def db_products_average_price():
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
            SELECT AVG(price) AS average_price
            FROM products;
            """

            cursor.execute(query)

            products = cursor.fetchall()

    except Error as e:
        print(f"Error while getting products from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return products

def db_products_not_ordered():
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
            SELECT p.id AS product_id, p.name AS product_name
            FROM products p
            LEFT JOIN order_item oi ON p.id = oi.product_id
            WHERE oi.product_id IS NULL;
            """

            cursor.execute(query)

            products = cursor.fetchall()

    except Error as e:
        print(f"Error while getting products from database: {e}")

    finally:
        cursor.close()
        connection.close() 
        return products

def create_db_products_bulk(products: List[ProductCreate]):
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

            for product in products:
                cursor.execute("SELECT id FROM categories WHERE id=%s", (product.category_id,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail=f"The category with id {product.category_id} does not exist.")

            query = f"""
            INSERT INTO products (name, description, price, stock, category_id) VALUES (%s, %s, %s, %s, %s)
            """

            for product in products:
                values = (product.name, product.description, product.price, product.stock, product.category_id)

                cursor.execute(query, values)

        connection.commit()

    except Error as e:
        print(f"Error while creating products in bulk: {e}")
        if connection:
            connection.rollback()
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

    return True

       

