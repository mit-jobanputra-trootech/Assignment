from core.base_models import UUIDBase
from sqlalchemy import Column, String


class User(UUIDBase):
    __tablename__ = "user"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    salt_password = Column(String(250), nullable=False)

