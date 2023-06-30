
import os
import random
import re
from time import time

from dotenv import load_dotenv
from fastapi import Body, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig
from jose import jwt
from sqlalchemy.orm import Session
from src.routers.Auth.models import User
from src.config.password_hashing import Hash
from src.config.auth import create_access_token

templates = Jinja2Templates(directory="templates")
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'




async def registration(form=None, db=None):
    if not form.password == form.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password not matched.")
    exits_user = db.query(User).filter(User.email == form.email).first()
    if exits_user:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail='User details already exists.')
    user = User(username=form.username, email=form.email, password=Hash.get_hash_pass(form.password))
    if not re.fullmatch(regex, form.email):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email valid email id")
    # data = {"sub": user.email, "expiry": time() + 600}
    token = create_access_token(user.email)
    # template = env.get_template(f'verification.html')
    # html = template.render(
    #     url=f"http://localhost:3000/userauth/verification?token={jwt_token}",
    #     email=user.name,
    #     subject=f"Verification Mail"
    # )
    # message = MessageSchema(
    #     subject="Account Verification Email",
    #     recipients=[user.email],  # List of Recipients
    #     body=html,
    #     subtype="html"
    # )
    # fm = FastMail(conf)
    # if not fm:
    #     raise HTTPException(status_code=status.HTTP_226_IM_USED,
    #                         detail="Email Already Exits Please do Registration to another Email")
    # await fm.send_message(message)
    db.add(user)
    db.commit()
    db.refresh(user)
    return token



async def user_login(form=None, db=None):
    exists_user = db.query(User).filter(User.email == form.username)
    if not exists_user.first().is_active == True:
        exists_user.delete()
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Validation not completed')
    user = db.query(User).filter(User.email == form.username and User.is_active == True).first()
    if not Hash.verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password please enter valid password"
        )
    if len(form.password) < 6:
        return {"error": "Password is less than 6 Character, Please enter Password more thane 6 Character"}
    if not re.fullmatch(regex, form.username):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Invalid email please enter valid '
                                                                           'email.')
    jwt_token = create_access_token(form.username)
    # response.set_cookie(key="access_token", value=f"Bearer {jwt_token}", httponly=True)
    return jwt_token