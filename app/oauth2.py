from base64 import encode
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes





def create_access_token(data: dict):
    to_encode = data.copy()

    # expired time 30 minutes after creation
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt




def verify_access_token(token: str, credentials_exception):
    try:
        # decode the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the id
        id: str = payload.get("user_id")

        # If there is no id throw an error
        if id is None:
            raise credentials_exception

        # validate with a schema the actual token data
        token_data = schemas.TokenData(id=id)

    # if time has expired
    except JWTError:
        raise credentials_exception


    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    # credentials exception is fed into verify_access_token
    credentials_exception = HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Could not validate credential',
                            headers={"WWW-Authenticate": "Bearer"})


    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    #return verify_access_token(token, credentials_exception)

    return user