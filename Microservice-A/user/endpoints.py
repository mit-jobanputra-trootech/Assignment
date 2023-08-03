from datetime import timedelta

from core.config import config
from typing import List
from core.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from user.models import User
from user.utils import get_current_user
from user.crud import user as user_crud
from user.schemas import (Token, UserLogin,
                          UserRegistrationRequestData,
                          UserRegistrationResponseData,
                          FilterRequestData
                          )
from user.utils import authenticate_user, create_access_token

router = APIRouter()


@cbv(router)
class UserCBV:
    session: Session = Depends(get_db)

    @router.post(
        "/register", response_model=UserRegistrationResponseData, status_code=201
    )
    def register_user(self, user_request_data_schema: UserRegistrationRequestData):
        return user_crud.create(self.session, user_request_data_schema)

    @router.post("/login", response_model=Token)
    def login_for_access_token(
        self,
        login_form_data: UserLogin,
    ):
        user = authenticate_user(
            self.session, login_form_data.username, login_form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}


@cbv(router)
class UserListingCBV:
    session: Session = Depends(get_db)
    logged_in_user: User = Depends(get_current_user)

    @router.get(
        "/listing", status_code=200, response_model=List[UserRegistrationResponseData]
    )
    def users_listing(self, user_listing_schema: FilterRequestData):
        return user_crud.get_multi(self.session,
                                   offset=((user_listing_schema.page_number - 1) * user_listing_schema.page_size),
                                   limit=user_listing_schema.page_size)







