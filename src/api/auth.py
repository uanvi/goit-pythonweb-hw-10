from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.core.database import get_db
from src.core.config import settings
from src.core.auth import create_access_token
from src.core.dependencies import get_current_user
from src.schemas.user import UserCreate, UserLogin, UserResponse, Token
from src.crud import user as crud_user
from src.services.email import send_verification_email

# Cloudinary configuration
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Перевірити чи існує користувач
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    new_user = crud_user.create_user(db=db, user=user)
    
    try:
        await send_verification_email(new_user.email, new_user.id)
    except Exception as e:
        print(f"Failed to send verification email: {e}")
    
    return new_user

@router.post("/login", response_model=Token)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@router.post("/verify/{user_id}")
def verify_email(user_id: int, db: Session = Depends(get_db)):
    """Верифікувати email користувача"""
    success = crud_user.verify_user_email(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "Email verified successfully"}

@router.post("/avatar", response_model=UserResponse)
def upload_avatar(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Завантажити аватар користувача"""
    try:
        # Завантажити файл до Cloudinary
        result = cloudinary.uploader.upload(
            file.file,
            folder="avatars",
            public_id=f"avatar_{current_user.id}",
            overwrite=True,
            transformation=[
                {"width": 200, "height": 200, "crop": "fill"}
            ]
        )
        
        # Оновити URL аватара в базі даних
        updated_user = crud_user.update_user_avatar(
            db, current_user.id, result["secure_url"]
        )
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return updated_user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading avatar: {str(e)}"
        )
    # Перевірити чи існує користувач
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    return crud_user.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    return current_user