from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserProfile, UserAddress, UserAddressCreate, UserUpdate
from crud.users import get_user_profile, create_user_address, get_user_by_email, update_user_profile
from models import User_address

router = APIRouter(prefix="/users", tags=["users"])

# Эндпоинт для получения профиля пользователя по email
@router.get("/lk", response_model=UserProfile)
def get_profile_by_email(
    email: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        user = get_user_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        profile = get_user_profile(db, user.id)
        return profile
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении профиля: {str(e)}"
        )
        
        
@router.put("/profile", response_model=UserProfile)
def update_profile(
    user_data: UserUpdate,
    email: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        updated_user = update_user_profile(db, email, user_data)

        profile = get_user_profile(db, updated_user.id)
        return profile
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении профиля: {str(e)}"
        )

# Эндпоинт для создания нового адреса пользователя
@router.post("/addresses", response_model=UserAddress, status_code=status.HTTP_201_CREATED)
def create_address_for_user(
    address: UserAddressCreate,
    email: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        user = get_user_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        return create_user_address(db, address, user.id)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании адреса: {str(e)}"
        )

# Эндпоинт для удаления адреса пользователя
@router.delete("/addresses/{address_id}")
def delete_address_by_email(
    address_id: int,
    email: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        user = get_user_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        address = db.query(User_address).filter(
            User_address.user_id == user.id,
            User_address.id == address_id
        ).first()
        
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Адрес не найден"
            )

        db.delete(address)
        db.commit()
        
        return {"message": "Адрес успешно удален"}
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении адреса: {str(e)}"
        )