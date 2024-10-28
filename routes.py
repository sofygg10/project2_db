from fastapi import APIRouter, HTTPException
from models import CustomerCreate
from db_customers_helper import db_customers_get, create_db_customer, create_db_customers_bulk
from typing import List 

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

