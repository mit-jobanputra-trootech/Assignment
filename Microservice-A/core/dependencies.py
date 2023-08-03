from database import Session


def get_db():
    """Returns database session"""
    db = Session()
    try:
        yield db
    finally:
        db.close()
