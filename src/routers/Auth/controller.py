from fastapi import APIRouter, Depends, Body, File, UploadFile
from sqlalchemy.orm.session import Session
from src.config.db_config import get_db
from celery.result import AsyncResult
from starlette.responses import JSONResponse
from src.routers.Auth.tasks import operation_task
from src.routers.Auth.schemas import CeleryTest, UserRegistrationSchema, UserLoginSchema, EmailSchema, VerifyOTP, ResetPassword, DisplayUserSchema, UserIn, BaseUser
from src.routers.Auth.services import registration, user_login, forgot_Password, verify_otp, reset_password, get_all_user, addProfileImage
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.config.auth import get_current_user

router = APIRouter(
    prefix='/api', tags=[f'Auth'], responses={404: {"description": "Not found"}})


@router.post("/signup")
async def user_registration(form: UserRegistrationSchema = Body(default=None), db: Session = Depends(get_db)):
    """For registration please follow the given requirements"""
    response = await registration(form=form, db=db)
    return {"token": response}


@router.post('/signin')
async def user_signup(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """For login please fill validate data."""
    access_token = await user_login(form, db)
    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }

@router.post('/forget-password')
async def password_Forget(form: EmailSchema = Body(), db:Session = Depends(get_db)):
    """Forget password"""
    return forgot_Password(db, form)

@router.post('/verify-otp')
async def verify_Otp(form: VerifyOTP = Body(default=None), db: Session = Depends(get_db)):
    """Verify Otp"""
    return verify_otp(form, db)

@router.post("/reset-password")
async def reset_Password(form: ResetPassword = Body(default=None), db: Session = Depends(get_db)):
    return reset_password(form, db)


@router.get('/user', response_model= list[DisplayUserSchema])
def getUsers(db:Session = Depends(get_db)):
    return get_all_user(db)

# Single image file upload
@router.post('/add-profile-image')
async def add_profile_image(file: UploadFile = File(...)):
    response = await addProfileImage(file)
    return response

@router.post("/operation")
async def get_mathmetic_result(form: CeleryTest, token: str = Depends(get_current_user)):
    if form:
        task = operation_task.apply_async(args=(form.num1, form.num2, form.Operation))
        return JSONResponse({"task_id": task.id})


@router.get("/result/{task_id}")
async def result(task_id: str):
    task = AsyncResult(task_id)

    # Task Not Ready
    if not task.ready():
        return {"status": task.status}

    # Task done: return the value
    task_result = task.get()
    return JSONResponse({"task_id": str(task_id),
                         "status": task.status,
                         "result": task_result
                         })


@router.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user