from core.config import config
from fastapi import FastAPI
from user import endpoints as user_endpoints


app = FastAPI(title="Microservice-A", docs_url="/docs", debug=config.DEBUG)


app.include_router(
    user_endpoints.router, prefix=f"{config.API_V1_STR}/users", tags=["Users"]
)

