from fastapi import APIRouter, Body, Query, Depends, UploadFile, File, Response
from sqlalchemy.orm.session import Session
from src.config.db_config import get_db
from src.config.auth import get_current_user
from src.routers.Product.schemas import AddProductSchema, DisplayProductShema, DeleteProductShema
from src.routers.Product.models import Product
from src.routers.Product.services import addproduct, showAllProduct, getProduct, updateProduct, deleteProducts, deleteSingleProduct, addProductImages
from src.config.configuration import ODOO_URL, ODOO_DB, ODOO_DB_USER, ODOO_DB_PASS
from typing import List
import aiofiles
import xmlrpc.client


url = ODOO_URL
db = ODOO_DB
# odoo web credentials username and passswod
username = ODOO_DB_USER
password = ODOO_DB_PASS

router = APIRouter(prefix="/api/product",
                   tags=[f'Product'], responses={404: {"description": "Not found"}})


@router.post("/create-product")
async def add_product(form: AddProductSchema = Body(default=None), db: Session = Depends(get_db), logged_user: Session = Depends(get_current_user)):
    response = addproduct(form, db, logged_user)
    return response


# Multiple image files uploaded
@router.post("/upload-product-image")
async def create_upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db), pid: int = Query(default=None), token: Session = Depends(get_current_user)):
    result = await addProductImages(db, files, pid, token)
    return result


@router.post('/show-products')
async def all_products(db: Session = Depends(get_db)):
    response = showAllProduct(db)
    return response


@router.post('/get-product')
async def get_Product(db: Session = Depends(get_db), pid: int = Query(default=None), token: Session = Depends(get_current_user)):
    result = getProduct(db, pid, token)
    return result


@router.put('/update-product')
async def update_product(db: Session = Depends(get_db), pid: int = Query(default=None), form: AddProductSchema=Body(default=None), token: Session = Depends(get_current_user)):
    result = updateProduct(db, pid, form, token)
    return result

@router.delete('/delete-products')
async def delete_Products(db:Session = Depends(get_db), pid: DeleteProductShema = Body(default=None), token: Session=Depends(get_current_user)):
    result = deleteProducts(db, pid, token)
    return result

@router.delete('/delete-product')
async def delete_single_product(db: Session = Depends(get_db), pid: int = Query(default=None), token: Session = Depends(get_current_user)):
    result = deleteSingleProduct(db, pid, token)
    return result

# Odoo api
@router.post("/odoo-api")
def odoo_external_api():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    try:
        uid = common.authenticate(db, username, password, {})
        if uid:
            models = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/object'.format(url))
            # search methods
            partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [
                                         [['is_company', '=', True]]])
            # read methods
            partners_rec = models.execute_kw(db, uid, password, 'res.partner', 'read', [
                                             partners], {'fields': ['id', 'email']})
            return {"message": 'authentication successfull', "data": partners_rec}

        else:
            return {"message": 'authentication unsuccessfull'}
    except:
        return {"message": "Server down please retry after 1 hours"}
