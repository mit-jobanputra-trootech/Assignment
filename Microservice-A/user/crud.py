import uuid

from core.crud_base import CRUDBase
from sqlalchemy.orm import Session
from user.models import User
from user.schemas import UserRegistrationRequestData, UserRegistrationCRUDData
from user.utils import hash_new_password


class CRUDUser(CRUDBase[User, [], []]):
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, obj_in: UserRegistrationRequestData) -> User:
        # hash the password before saving it to database
        salt_password, obj_in.password = hash_new_password(obj_in.password)
        obj_in.email = obj_in.email.lower()
        user_registration_schema = UserRegistrationCRUDData(**obj_in.dict(),
                                                            salt_password=salt_password,
                                                            id=str(uuid.uuid4()))
        return super().create(db, obj_in=user_registration_schema)


user = CRUDUser(User)
