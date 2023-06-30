from typing import List, Optional

from pydantic import EmailStr, BaseModel, validator, Field

class CeleryTest(BaseModel):
    num1: float
    num2: float
    Operation: str

    class Config:
        orm_mode: True

# User Schema
class UserRegistrationSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    class Config:
        orm_mode: True
        schema_extra = {
            "example": {
                "username": "Dipu12345",
                "email": "dipu@yopmail.com",
                "password": "Dipu12345@",
                "confirm_password": "Dipu12345@"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        orm_mode: True
        schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any"
            }
        }