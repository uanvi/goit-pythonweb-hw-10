from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.auth import verify_token
from src.crud.user import get_user_by_email
from src.models.user import User

security = HTTPBearer()

def get_current_user(
    token: str = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    # Отримати токен з Bearer схеми
    credentials = token.credentials
    email = verify_token(credentials)
    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user