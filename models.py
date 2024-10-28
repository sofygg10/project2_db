from pydantic import BaseModel, Field

class CustomerCreate(BaseModel):
    name:str = Field(..., description= "nombre requerido")
    email:str =  Field(..., description= "email requerido")
    phone:str = Field(..., description= "phone requerido")
    address: str

class CategoryCreate(BaseModel):
    name: str
    description: str
    
