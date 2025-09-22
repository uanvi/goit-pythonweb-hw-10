from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate
from src.core.auth import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def verify_user_email(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        user.is_verified = True
        db.commit()
        return True
    return False

def update_user_avatar(db: Session, user_id: int, avatar_url: str):
    user = get_user_by_id(db, user_id)
    if user:
        user.avatar_url = avatar_url
        db.commit()
        db.refresh(user)
        return user
    return None