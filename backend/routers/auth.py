from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from schemas import UserRegister, Token, ChangePassword, UserLogin
from crud.users import create_user, authenticate_user, update_user_password
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

# "Эндпоинт для обработки запросов аутентификации
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        user = create_user(db, user_data)
        return {
            "message": "Пользователь успешно создан", 
            "user_id": user.id,
            "email": user.email
        }
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании пользователя: {str(e)}"
        )

# Эндпоинт для входа пользователя в систему
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):
    
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный адрес электронной почты или пароль"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token, 
            "token_type": "bearer"
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка входа в систему: {str(e)}"
        )

@router.post("/login-json", response_model=Token)
def login_json(
    login_data: UserLogin,
    db: Session = Depends(get_db)
    ):
    try:
        user = authenticate_user(db, login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный адрес электронной почты или пароль"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token, 
            "token_type": "bearer"
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка входа в систему: {str(e)}"
        )

# Эндпоинт для изменения пароля пользователя
@router.post("/change-password")
def change_password(
    password_data: ChangePassword,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    try:
        user = update_user_password(db,  current_user.id, password_data)
        return {"message": "Пароль успешно изменен"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при смене пароля: {str(e)}"
        )
