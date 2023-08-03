import requests
import json
from core.dependencies import get_db
from core.config import config
from fastapi import APIRouter, Depends, Header
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from user.schemas import (FilterRequestData, UserRegistrationRequestData, UserLogin)

router = APIRouter()


@cbv(router)
class UserCBV:
    session: Session = Depends(get_db)

    @router.post(
        "/insert-user", status_code=201
    )
    def insert_user_in_db(self, user_request_data_schema: UserRegistrationRequestData):
        url = f"{config.MICROSERVICE_A_ENDPOINT}/api/v1/users/register"

        payload = json.dumps(user_request_data_schema.dict())
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(response.content)

    @router.post("/generate-access-token")
    def generate_access_token(
            self,
            login_form_data: UserLogin,
    ):
        url = f"{config.MICROSERVICE_A_ENDPOINT}/api/v1/users/login"

        payload = json.dumps(login_form_data.dict())
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(response.content)

    @router.post("/fetch-user-listing")
    def fetch_user_listing(
            self,
            user_listing_schema: FilterRequestData,
            token: str = Header()
    ):
        url = f"{config.MICROSERVICE_A_ENDPOINT}/api/v1/users/listing"

        payload = json.dumps(user_listing_schema.dict())
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {token}"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return json.loads(response.content)











