from fastapi import APIRouter, HTTPException
from models import CustomerCreate
from db_customers_helper import db_customers_get

router = APIRouter()

@router.get("/get/customers")
def get_customers ():
    customers = db_customers_get()
    return{
        "customers" : customers
    }

