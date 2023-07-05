from fastapi import APIRouter, Body, Query, Depends
from sqlalchemy.orm.session import Session
from src.config.db_config import get_db
from src.config.auth import get_current_user
from src.routers.Product.schemas import AddProductSchema
from src.routers.Product.models import Product
from src.routers.Product.services import addproduct

router = APIRouter(prefix="/api/product", tags=[f'Product'], responses={404: {"description": "Not found"}})

@router.post("add-product", tags=["Product"])
def add_product(form: AddProductSchema = Body(default=None), db: Session = Depends(get_db), logged_user: Session = Depends(get_current_user)):
    response = addproduct(form, db, logged_user)
    return response
