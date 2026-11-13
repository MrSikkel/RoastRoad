"""Роутер профиля пользователя и адресов."""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..deps import get_current_user, get_db
from ..models.user import User

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.put("/me", response_model=schemas.UserOut)
def update_me(
    payload: schemas.UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    return crud.user.update(db, current_user, payload.model_dump(exclude_unset=True))


@router.get("/addresses", response_model=list[schemas.AddressOut])
def list_addresses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list:
    return crud.address.list_addresses(db, current_user.id)


@router.post(
    "/addresses",
    response_model=schemas.AddressOut,
    status_code=status.HTTP_201_CREATED,
)
def create_address(
    payload: schemas.AddressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.address.create(db, current_user.id, payload.model_dump())


@router.put("/addresses/{address_id}", response_model=schemas.AddressOut)
def update_address(
    address_id: int,
    payload: schemas.AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    address = crud.address.get_address(db, current_user.id, address_id)
    return crud.address.update(db, address, payload.model_dump(exclude_unset=True))


@router.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    address = crud.address.get_address(db, current_user.id, address_id)
    crud.address.delete(db, address)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
