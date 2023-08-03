from datetime import datetime, timedelta

from core.config import config
from core.dependencies import get_db
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              OAuth2PasswordBearer)
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Tuple
import hashlib
import hmac
import uuid

security = HTTPBearer()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(db, username: str, password: str):
    from user.crud import user as user_crud

    user = user_crud.get_user_by_username(db, username)
    if not user:
        return False
    if not is_correct_password(user.salt_password, user.password, password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def get_current_user(
    authorization: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    from user.crud import user

    try:
        token = authorization.credentials
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_in_db = user.get_user_by_username(session, username)
    if user_in_db is None:
        raise credentials_exception
    return user_in_db


def hash_new_password(password: str) -> Tuple[str, str]:
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    salt = uuid.uuid4().hex
    pw_hash = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return salt, pw_hash


def is_correct_password(salt: str, pw_hash: bytes, password: str) -> bool:
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    return hmac.compare_digest(
        pw_hash,
        hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    )



