from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserProfile, UserAddress, UserAddressCreate, UserUpdate
from crud.users import get_user_profile, create_user_address, get_user_addresses, update_user_profile
from models import User_address
from auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/lk", response_model=UserProfile)
def get_profile(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        profile = get_user_profile(db, current_user.id)
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
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    try:
        updated_user = update_user_profile(db, current_user.id, user_data)
        profile = get_user_profile(db, updated_user.id)
        return profile
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении профиля: {str(e)}"
        )

@router.get("/addresses", response_model=list[UserAddress])
def get_addresses(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    try:
        addresses = get_user_addresses(db, current_user.id)
        return addresses
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении адресов: {str(e)}"
        )

@router.post("/addresses", response_model=UserAddress, status_code=status.HTTP_201_CREATED)
def create_address(
    address: UserAddressCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    try:
        return create_user_address(db, address, current_user.id)
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании адреса: {str(e)}"
        )

# Эндпоинт для удаления адреса пользователя
@router.delete("/addresses/{address_id}")
def delete_address(
    address_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    try:
        address = db.query(User_address).filter(
            User_address.user_id == current_user.id,
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