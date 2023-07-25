import time
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from src.config.configuration import setting, ALGO
from src.config.db_config import get_db
from src.routers.Auth.models import User

JWT_SECRET = setting.SECRET_KEY
JWT_ALGORITHM = ALGO
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/user/signin')


# function used for signing the JWT string
def create_access_token(username=None):
    payload = {
        "user": username,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        verified = jwt.decode(token, setting.SECRET_KEY,
                              algorithms=setting.ALGORITHM)
        if not verified['expiry'] >= time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Session Expired. !!!!")
        username = verified['user']
        user = db.query(User).filter(User.email == username and User.is_active == True).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Credentials Invalid. !!!!")
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credentials Invalid. !!!!")
