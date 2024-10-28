from fastapi import APIRouter, HTTPException
from models import CustomerCreate, CategoryCreate, ProductCreate, OrderCreate, OrderItemCreate, ShippingStateCreate
from db_customers_helper import db_customers_get, create_db_customer, create_db_customers_bulk
from typing import List 
from db_category_helper import create_db_category, db_get_categories, create_db_categories_bulk
from db_products_helper import db_product_create, db_products_get, create_db_products_bulk
from db_orders_helper import db_order_create, db_orders_get, create_db_orders_bulk
from db_order_item_helper import db_order_item_create, db_order_item_get, create_db_order_item_bulk
from db_shipping_state_helper import db_shipping_state_create, db_shipping_status_get

router = APIRouter()

@router.get("/get/customers")
def get_customers ():
    customers = db_customers_get()
    return{
        "customers" : customers
    }

@router.post("/create/customer")
def create_customer (customer: CustomerCreate):
    create_db_customer(customer)
    return{
        "message" : "Customer created successfully"
    }

@router.post("/create/customer/bulk")
def bulk_customer (customers: List[CustomerCreate]):
    if create_db_customers_bulk (customers):
        return{
            "message" : "Customers created successfully"
        }
    else:
        raise HTTPException(status_code=500, detail="An error occurred while creating customers.")

@router.post("/create/category")
def create_category (category: CategoryCreate):
    create_db_category(category)

    return{
        "message": "Category created successfully."
    }

@router.get("/get/categories")
def get_categories ():
    categories = db_get_categories()
    return {
        "categories": categories
    }

@router.post("/create/categories/bulk")
def bulk_categories(categories: List[CategoryCreate]):
    if create_db_categories_bulk (categories):
        return{
            "message" : "Categories created successfully"
        }
    else:
        raise HTTPException(status_code=500, detail="An error occurred while creating categories.")


@router.post("/create/product")
def create_product(product: ProductCreate):
    db_product_create(product)

    return {
        "message": "Product created successfully"
    }

@router.get("/get/products")
def get_products():
    products = db_products_get()
    return {
        "products": products
    }

@router.post("/create/products/bulk")
def bulk_products(products: List[ProductCreate]):
    if create_db_products_bulk (products):
        return{
            "message" : "Products created successfully"
        }
    else:
        raise HTTPException(status_code=500, detail="An error occurred while creating products.")

@router.post("/create/order")
def create_order(order: OrderCreate):
    db_order_create(order)
    return {
        "message": "Order created successfully"
    }

@router.get("/get/orders/")
def get_orders():
    orders = db_orders_get()

    return {
        "orders" : orders 
    }

@router.post("/create/orders/bulk")
def bulk_orders (orders: List[OrderCreate]):
    if create_db_orders_bulk (orders):
        return{
            "message" : "Orders created successfully"
        }
    else:
        raise HTTPException(status_code=500, detail="An error occurred while creating orders.")

@router.post("/create/order-item")
def create_order_item(order_item : OrderItemCreate):
    db_order_item_create(order_item)
    return {
        "message": "Order item created successfully"
    }


@router.get("/get/order-item")
def get_order_item():
    order_item = db_order_item_get()
    print(order_item)
    return {
        "order_item" : order_item
    }

@router.post("/create/order-item/bulk")
def order_item_bulk(order_item : List[OrderItemCreate]):
    if  create_db_order_item_bulk (order_item):
        return{
            "message" : "Orders item created successfully"
        }
    else:
        raise HTTPException(status_code=500, detail="An error occurred while creating orders item.")

@router.post("/create/shipping-status")
def create_shipping_status(shipping_state: ShippingStateCreate):
    db_shipping_state_create(shipping_state)
    return {
        "message": "Shipping state created successfully"
    }

@router.get("/get/shipping-status")
def get_shipping_status():
    shipping_status = db_shipping_status_get()

    return {
        " shipping_status" :  shipping_status
    }














    


