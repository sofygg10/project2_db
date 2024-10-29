from fastapi import APIRouter, HTTPException
from models import CustomerCreate, CategoryCreate, ProductCreate, OrderCreate, OrderItemCreate, ShippingStateCreate
from db_customers_helper import db_customers_get, create_db_customer, create_db_customers_bulk, db_customers_get_orders, db_highest_per_customer_get, db_without_orders_get, db_customers_highest_order
from typing import List 
from db_category_helper import create_db_category, db_get_categories, create_db_categories_bulk, db_get_total_by_category
from db_products_helper import db_product_create, db_products_get, create_db_products_bulk, db_products_categories_get, db_products_average_price, db_products_not_ordered
from db_orders_helper import db_order_create, db_orders_get, create_db_orders_bulk, db_most_recent_per_customer
from db_order_item_helper import db_order_item_create, db_order_item_get, create_db_order_item_bulk
from db_shipping_state_helper import db_shipping_state_create, db_shipping_status_get, db_orders_shipping_status

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


@router.get("/get/customer-orders")
def get_customer_orders(customer_id):
    customer_order = db_customers_get_orders(customer_id)
    return {
        "orders" : customer_order
    }

@router.get("/get/products/categories")
def get_products_categories():
    products = db_products_categories_get()
    return {
        "Products" : products
    }

@router.get("/get/orders/highest-per-customer")
def highest_per_customer():
    customers = db_highest_per_customer_get()
    return {
        "customers" : customers
    }

@router.get("/get/customers/without-orders")
def without_orders():
    customers = db_without_orders_get()
    return {
        "customers" : customers
    }

@router.get("/get/sales/total-by-category")
def sales_total_by_category ():
    sales = db_get_total_by_category()
    return {
        "sales" : sales
    }

@router.get("/get/orders/most-recent-per-customer")
def most_recent_per_customer ():
    orders = db_most_recent_per_customer()
    return {
        "orders" : orders
    }

@router.get("/get/products/average-price")
def products_average_price ():
    average_price = db_products_average_price()
    return {
        "average_price" : average_price
    }

@router.get("/get/orders/shipping_status")
def orders_shipping_status ():
    shipping_status = db_orders_shipping_status()
    return {
        "shipping_status" : shipping_status
    }

@router.get("/get/products/not-ordered")
def products_not_ordered():
    not_ordered = db_products_not_ordered()
    return {
        "not_ordered" : not_ordered
    }
@router.get("/get/customers/highest-order")
def customers_highest_order():
    customer = db_customers_highest_order()
    return {
        "customer" : customer
    }















    


