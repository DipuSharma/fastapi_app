import os
from fastapi import HTTPException, status
from src.routers.Product.models import Product
from src.routers.Auth.models import User
from src.config.configuration import HOST

def disc_price(li_price, sell_price):
    discount = int(((li_price - sell_price) / li_price) * 100)
    return discount


def addproduct(form, db, user):
    get_user_id = db.query(User).filter(User.email == user.email).first()
    existing_data = db.query(Product).filter(Product.batch_No == form.batch_No and Product.company_name ==
                                             form.company_name and Product.user_id == get_user_id).first()
    if existing_data:
        return {"status": "failed", "message": "Product details already exists.", "data": form}
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


def showAllProduct(db):
    products = db.query(Product).all()
    return [{"product_name": record.product_name, "company_name": record.company_name, "batch_No": record.batch_No, 'selling_price': record.selling_price, 'list_price': record.list_price, 'product_size':'', 'product_color': '', 'description': ''} for record in products]