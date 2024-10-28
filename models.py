from pydantic import BaseModel, Field
from typing import Literal

class CustomerCreate(BaseModel):
    name:str = Field(..., description= "nombre requerido")
    email:str =  Field(..., description= "email requerido")
    phone:str = Field(..., description= "phone requerido")
    address: str

class CategoryCreate(BaseModel):
    name: str
    description: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: int

class OrderCreate(BaseModel):
    customer_id: int
    total: float
    state: Literal['pending', 'completed', 'cancelled'] = 'pending'
    
