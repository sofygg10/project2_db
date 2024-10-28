from fastapi import APIRouter, HTTPException
from models import CustomerCreate, CategoryCreate
from db_customers_helper import db_customers_get, create_db_customer, create_db_customers_bulk
from typing import List 
from db_category_helper import create_db_category, db_get_categories, create_db_categories_bulk

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





