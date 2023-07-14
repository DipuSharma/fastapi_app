from fastapi import APIRouter, Body, Query, Depends, UploadFile, File, Response
from sqlalchemy.orm.session import Session
from src.config.db_config import get_db
from src.config.auth import get_current_user
from src.routers.Product.schemas import AddProductSchema, DisplayProductShema
from src.routers.Product.models import Product
from src.routers.Product.services import addproduct, showAllProduct
from src.config.configuration import ODOO_URL, ODOO_DB, ODOO_DB_USER, ODOO_DB_PASS
from typing import List
import aiofiles
import xmlrpc.client
url = ODOO_URL
db = ODOO_DB
# odoo web credentials username and passswod
username = ODOO_DB_USER
password = ODOO_DB_PASS

router = APIRouter(prefix="/api/product", tags=[f'Product'], responses={404: {"description": "Not found"}})

@router.post("/create-product")
async def add_product(form: AddProductSchema = Body(default=None), db: Session = Depends(get_db), logged_user: Session = Depends(get_current_user)):
    response = addproduct(form, db, logged_user)
    return response


# Multiple image files uploaded
@router.post("/upload-files")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        destination_file_path = "./static/image/"+file.filename #output file path
        async with aiofiles.open(destination_file_path, 'wb') as out_file:
            while content := await file.read(1024):  # async read file chunk
                await out_file.write(content)  # async write file chunk
    return {"Result": "OK", "filenames": [file.filename for file in files]}

@router.post('/show-product', response_model=List[DisplayProductShema] | None)
async def all_products(db: Session= Depends(get_db)):
    response = showAllProduct(db)
    return response


@router.post("/odoo-api")
def odoo_external_api():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    try:
        uid = common.authenticate(db, username, password, {})
        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            # search methods
            partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]])
            # read methods
            partners_rec = models.execute_kw(db, uid, password, 'res.partner', 'read', [partners], {'fields': ['id', 'email']})
            return {"message": 'authentication successfull', "data": partners_rec}
        
        else:
            return {"message": 'authentication unsuccessfull'}
    except:
        return {"message": "Server down please retry after 1 hours"}