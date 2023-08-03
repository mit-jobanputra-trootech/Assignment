from database import Base
from fastapi_utils.guid_type import GUID
from sqlalchemy import Column


class UUIDBase(Base):
    __abstract__ = True

    id = Column(GUID, primary_key=True)
