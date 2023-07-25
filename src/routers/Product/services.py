import os
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.routers.Product.models import Product, ProductImage
from src.routers.Auth.models import User
from src.config.configuration import HOST
from sqlalchemy import join
import aiofiles
def disc_price(li_price, sell_price):
    try:
        discount = int(((li_price - sell_price) / li_price) * 100)
        return discount
    except:
        return 0


def addproduct(form, db, user):
    get_user_id = db.query(User).filter(User.email == user.email).first()
    existing_data = db.query(Product).filter(Product.batch_No == form.batch_No and Product.company_name ==
                                             form.company_name and Product.user_id == get_user_id).first()
    if existing_data:
        return {"status": "failed", "message": "Product details already exists.", "data": existing_data}
    product = Product(product_name=form.product_name, company_name=form.company_name,
                      batch_No=form.batch_No, selling_price=form.selling_price,
                      list_price=form.list_price,
                      discount_price=disc_price(
                          form.list_price, form.selling_price),
                      product_size=form.product_size[0],
                      product_color=form.product_color[0],
                      description=form.description,
                      user_id=get_user_id.id)

    db.add(product)
    db.commit()
    db.refresh(product)
    return {"status": "success", "message": "Product added successfully", "data": form}

async def addProductImages(db, files, pid, token):
    existing_data = db.query(ProductImage).filter(ProductImage.product_id == pid).count()
    if existing_data > 5:
        return {'status': 'ok', 'message': 'no more image upload for this product'}
    for file in files:
        destination_file_path = "./static/image/"+file.filename  # output file path
        host_file_name =  HOST + destination_file_path[1:]
        product_images = ProductImage(product_image_path=host_file_name, product_id=pid)
        db.add(product_images)
        db.commit()
        db.refresh(product_images)
        async with aiofiles.open(destination_file_path, 'wb') as out_file:
            while content := await file.read(1024):  # async read file chunk
                await out_file.write(content)  # async write file chunk
    return {"status": "OK", "filenames": [file.filename for file in files]}

def showAllProduct(db):
    products = db.query(Product).all()
    # Many to Many Join Query
    for c, i in db.query(User, Product).filter(User.id == Product.user_id).all():
        pass
        # print ("ID: {} Name: {} Product name: {} Batch No: {}".format(c.id, c.username, i.product_name, i.batch_No))
    # Contains query
    s = db.query(Product).filter(Product.id.contains([3, 4, 5]))
    return [{"product_name": record.product_name,
             "company_name": record.company_name,
             "batch_No": record.batch_No,
             'selling_price': record.selling_price,
             'list_price': record.list_price,
             'discount': record.discount_price,
             'product_size': record.product_size,
             'product_color': record.product_color,
             'description': record.description,
             'images': [{'url': image.product_image_path} for image in db.query(ProductImage).filter(ProductImage.product_id == record.id).all()]} 
             for record in products]

def getProduct(db, pid, user=None):
    products = db.query(Product).filter(Product.id == pid).all()
    return products

def updateProduct(db, pid, form, token):
    existing_data = db.query(Product).filter(
        Product.id == pid and Product.user_id == token.id)
    if not existing_data.first():
        return {"status": 'failed', 'message': f'record not found of the id {pid}'}
    existing_data.update({Product.product_name: form.product_name, Product.company_name: form.company_name,
                          Product.batch_No: form.batch_No, Product.selling_price: form.selling_price,
                          Product.list_price: form.list_price,
                          Product.discount_price: disc_price(
                              form.list_price, form.selling_price),
                          Product.product_size: form.product_size[0],
                          Product.product_color: form.product_color[0],
                          Product.description: form.description,
                          Product.user_id: token.id})
    db.commit()
    return {"status": "ok", 'message': 'Product data updated successfully', 'data': existing_data.first()}

def deleteProducts(db, pids=None, token = None):
    existing_data = db.query(Product).filter(Product.id.in_(pids.products_id))
    if not existing_data.all():
        return {'status': 'failed', 'message':'record not found'}
    existing_data.delete()
    db.commit()
    return {'status': 'ok', 'message':'record successfylly deleted'}

def deleteSingleProduct(db, pid, token):
    existing_data = db.query(Product).filter(Product.id == pid and Product.user_id == token.id)
    if not existing_data.first():
        return {'status': 'failed', 'message':'record not found'}
    existing_data.delete()
    db.commit()
    return {'status': 'ok', 'message':'record successfylly deleted'}