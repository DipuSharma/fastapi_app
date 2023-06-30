from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.config.db_config import get_db
from celery.result import AsyncResult
from starlette.responses import JSONResponse
from src.routers.Auth.tasks import operation_task
from src.routers.Auth.schema import CeleryTest, UserRegistrationSchema, UserLoginSchema
from src.routers.Auth.services import registration, user_login
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.config.auth import get_current_user

router = APIRouter(
    prefix='/api', tags=[f'Auth'], responses={404: {"description": "Not found"}})


@router.post("/signup")
async def user_registration(form: UserRegistrationSchema, db: Session = Depends(get_db)):
    """For registration please follow the given requirements"""
    response = await registration(form=form, db=db)
    return {"token": response}


@router.post('/signin')
async def user_signup(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """"""
    access_token = await user_login(form, db)
    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }


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
