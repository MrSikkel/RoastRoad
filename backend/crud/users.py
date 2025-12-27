from sqlalchemy.orm import Session
from typing import List, Optional
from models import User, User_address
from schemas import UserRegister, UserAddressCreate, ChangePassword, UserUpdate
from auth import get_password_hash, verify_password
from fastapi import HTTPException, status

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка в базе данных: {str(e)}"
        )

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка в базе данных: {str(e)}"
        )

def create_user(db: Session, user_data: UserRegister) -> User:
    try:
        db_user = get_user_by_email(db, email=user_data.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Адрес электронной почты уже зарегистрирован"
            )
        
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            last_name=user_data.last_name or "",
            first_name=user_data.first_name or "",
            patronymic=user_data.patronymic,
            phone=user_data.phone
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании пользователя: {str(e)}"
        )

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    try:
        user = get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка аутентификации: {str(e)}"
        )

def update_user_password(
    db: Session,
    user_id: int,
    password_data: ChangePassword
    ) -> User:
    
    try:
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        if not verify_password(password_data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текущий пароль введён неверено"
            )

        user.password_hash = get_password_hash(password_data.new_password)
        db.commit()
        db.refresh(user)
        return user
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сбросе пароля: {str(e)}"
        )

def get_user_profile(db: Session, user_id: int) -> dict:
    try:
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        return {
            "id": user.id,
            "email": user.email,
            "last_name": user.last_name,
            "first_name": user.first_name,
            "patronymic": user.patronymic,
            "phone": user.phone,
            "role": user.role.value,
            "registration_date": user.registration_date,
            "addresses": user.addresses,
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении профиля: {str(e)}"
        )

def update_user_profile(
    db: Session, 
    user_id: int,
    user_data: UserUpdate
    ) -> User:
    
    try:
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if value is not None:
                setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении профиля: {str(e)}"
        )

def create_user_address(
    db: Session, 
    address: UserAddressCreate, 
    user_id: int
    ) -> User_address:
    
    try:
        if address.is_current:
            db.query(User_address).filter(User_address.user_id == user_id, User_address.is_current == True).update({"is_current": False})
        
        db_address = User_address(**address.model_dump(), user_id=user_id)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании адреса: {str(e)}"
        )

def get_user_addresses(db: Session, user_id: int) -> List[User_address]:
    try:
        return db.query(User_address).filter(
            User_address.user_id == user_id).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении адресов: {str(e)}"
        )
