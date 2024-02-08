from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_hero.database import get_session
from fast_hero.models import User
from fast_hero.schemas import TokenData

SECRET_KEY = 'your-secret-key'  # Provisorio
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


# Recebe uma senha em texto puro como argumento e retorna uma versão criptografada dessa senha
def get_password_hash(password: str):
    return pwd_context.hash(password)


# Recebe uma senha em texto puro e uma senha criptografada como argumentos, e verifica se a senha em texto puro, quando criptografada, corresponde à senha criptografada. Ambas as funções utilizam o objeto pwd_context, que definimos anteriormente usando a biblioteca passlib
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.email == token_data.username)
    )

    if user is None:
        raise credentials_exception

    return user
