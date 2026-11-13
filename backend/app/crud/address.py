"""CRUD для адресов пользователя."""

from sqlalchemy.orm import Session

from ..errors import ConflictError, NotFoundError
from ..models.address import UserAddress
from ..models.order import Order


def list_addresses(db: Session, user_id: int) -> list[UserAddress]:
    return db.query(UserAddress).filter(UserAddress.user_id == user_id).all()


def get_address(db: Session, user_id: int, address_id: int) -> UserAddress:
    address = (
        db.query(UserAddress)
        .filter(UserAddress.id == address_id, UserAddress.user_id == user_id)
        .first()
    )
    if address is None:
        raise NotFoundError("Адрес не найден")
    return address


def create(db: Session, user_id: int, data: dict) -> UserAddress:
    is_default = data.pop("is_default", False)
    is_first = (
        db.query(UserAddress).filter(UserAddress.user_id == user_id).count() == 0
    )
    if is_default or is_first:
        _unset_default(db, user_id)
        is_default = True
    address = UserAddress(user_id=user_id, is_default=is_default, **data)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def update(db: Session, address: UserAddress, data: dict) -> UserAddress:
    if data.get("is_default"):
        _unset_default(db, address.user_id)
    for field, value in data.items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    return address


def delete(db: Session, address: UserAddress) -> None:
    used = db.query(Order).filter(Order.address_id == address.id).first()
    if used is not None:
        raise ConflictError("Нельзя удалить адрес, который используется в заказах")
    db.delete(address)
    db.commit()


def _unset_default(db: Session, user_id: int) -> None:
    db.query(UserAddress).filter(
        UserAddress.user_id == user_id, UserAddress.is_default.is_(True)
    ).update({"is_default": False}, synchronize_session=False)
