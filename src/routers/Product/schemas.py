from typing import List, Optional

from pydantic import EmailStr, BaseModel, validator, Field


class ImageSchema(BaseModel):
    id: int
    url: List[str] = []

    class Congig:
        orm_mode: True


class AddProductSchema(BaseModel):
    product_name: str
    company_name: str
    batch_No: Optional[str]
    selling_price: Optional[float]
    list_price: Optional[float]
    product_size: Optional[str]
    product_color: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode: True
        schema_extra = {
            "example": {
                "product_name": "T-Shirt",
                "company_name": "Sparky",
                "batch_No": "TS001",
                "selling_price": 799,
                "list_price": 899,
                "product_size": "M",
                "product_color": "Red",
                "description": "Nice Product",
            }
        }

class DisplayProductShema(BaseModel):
    product_name: str
    company_name: str
    batch_No: str
    selling_price: float
    list_price: float
    product_size: str
    product_color: str
    description: str
    
    class Config:
        orm_mode: True

class DeleteProductShema(BaseModel):
    products_id : List[int] = []

    class Config:
        orm_mode: True
        schema_extra = {
            "example": {
                "products_id": [],
            }
        }