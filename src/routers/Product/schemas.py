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
    image: Optional[ImageSchema]

    class Config:
        orm_mode: True
        schema_extra = {
            "example": {
                "product_name": "string",
                "company_name": "string",
                "batch_No": "string",
                "selling_price": 0,
                "list_price": 0,
                "product_size": "string",
                "product_color": "string",
                "description": "string",
                "image": [{"id":"integer", "url": []}]
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
    images: List[ImageSchema] = []
    
    class Config:
        orm_mode: True