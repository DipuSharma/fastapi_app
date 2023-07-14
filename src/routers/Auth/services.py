
import os
import re
import shutil
import random
import aiofiles
from time import time
from dotenv import load_dotenv
from fastapi import Body, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig
from jose import jwt
from sqlalchemy.orm import Session
from src.routers.Auth.models import User, OTP
from src.config.password_hashing import Hash
from src.config.auth import create_access_token
from src.config.configuration import setting, HOST
from src.routers.Auth.tasks import uploadProfilePicture

templates = Jinja2Templates(directory="templates")
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


async def registration(form=None, db=None):
    if not form.password == form.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password not matched.")
    exits_user = db.query(User).filter(User.email == form.email).first()
    if exits_user:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail='User details already exists.')
    user = User(username=form.username, email=form.email,
                password=Hash.get_hash_pass(form.password))
    if not re.fullmatch(regex, form.email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email valid email id")
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Validation not completed')
    user = db.query(User).filter(
        User.email == form.username and User.is_active == True).first()
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


def forgot_Password(db=None, user=None):
    data = db.query(User).filter(
        User.email == user.email and User.is_active == True).first()
    if not data:
        return {"status": "failed", "message": "Details Not Found"}
    if not re.fullmatch(regex, user.email):
        return {"status": "failed", "message": "Invalid Email ID Please Enter Valid Email"}
    otp = ''.join([str(random.randint(0, 9)) for i in range(6)])
    user_entry = OTP(email=user.email, otp=otp, status= False,
                    exp_time=time() + 60, count_otp=1)
    otp_email = db.query(OTP).filter(OTP.email == user.email).first()
    existing_data = db.query(OTP).filter(OTP.email == user.email)
    if otp_email:
        num = int(otp_email.count_otp)
        if num < 3:
            num = num + 1
            existing_data.update(
                {"status":False, "otp": otp, "exp_time": time() + 60, "count_otp": num})
            db.commit()
            return {"status":"success", "message": "otp send on your mail id", "otp": otp}
        return {"status": "failed", "message":"your ip addresss is blocked"}

    db.add(user_entry)
    db.commit()
    db.refresh(user_entry)
        # message = MessageSchema(
        #     subject="MyApp Account Verification Email",
        #     recipients=[user.email],  # List of Recipients
        #     body=f"your otp is {otp}"
        # )
        # fm = FastMail(conf)
        # await fm.send_message(message)
    return {"status": "Ok", "message": "Otp send on your mail id", "Otp": otp}
        
def verify_otp(form=None, db=None):
    num = 1
    if not form:
        raise HTTPException(status_code=404, detail="Otp not found")
    data = db.query(OTP).filter(OTP.otp == form.otp).first()
    if not data:
        return {"status": "failed", "message": "Invalid OTP please enter valid Otp"}
    otp_db_time = float(data.exp_time)
    existing_data = db.query(OTP).filter(OTP.otp == form.otp)
    if data.otp == form.otp and otp_db_time >= time():
        data = {"sub": data.email, "expiry": time() + 600}
        jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
        existing_data.update({"status": True, "count_otp": num})
        db.commit()
        return {"status": "success", "message": "your otp verification successfully", "access-token": jwt_token}
    existing_data.update({"count_otp": num})
    db.commit()
    return {"status": "failed", "message": "your otp is expired......"}


def reset_password(form=None, db=None):
        verified = jwt.decode(form.token, setting.SECRET_KEY,
                              algorithms=setting.ALGORITHM)
        if verified['expiry'] >= time():
            email: str = verified.get("sub")
            existing_data = db.query(User).filter(
                User.email == email and User.is_active == True)
            if not existing_data.first():
                return {"status": "failed", "message": "Password Reset Failed"}

            if form.password != form.confirm_password:
                return {"status": "failed", "message": "Password and Confirm Password mismatch"}

            password = Hash.get_hash_pass(form.password)
            existing_data.update({"password": password})
            db.commit()
            return {"message": "Password Reset Successfully"}

async def addProfileImage(file):
    destination_file_path = "./static/image/profile/"+file.filename #output file path
    generated_url = f'{HOST}' + destination_file_path[1:]
    async with aiofiles.open(destination_file_path, 'wb') as out_file:
        shutil.copyfileobj(file.file, out_file)
    return {"Result": "OK", "url": generated_url}
    # result = await uploadProfilePicture(file)
    # profile = UserProfile(photo=profile_path, user_id=user.id)
    # db.add(profile)
    # db.commit()
    # image_upload.delay(file)
    # return result

def get_all_user(db=None):
    data = db.query(User).all()
    for record in data:
        return [{"username": record.username, "email": record.email, "is_active": record.is_active}]