from sqlalchemy.orm import Session
from typing import List, Optional
from models import Product
from schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException, status
import json
from decimal import Decimal

# Функция для получения продуктов
def get_products(db: Session, skip: int = 0, limit: int = 10) -> List[Product]:
    try:
        return db.query(Product).order_by(Product.created_at.desc()).offset(skip).limit(limit).all()
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Функция для получения продукта по id
def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    try:
        return db.query(Product).filter(Product.id == product_id).first()
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Функция для создания нового продукта
def create_product(db: Session, product_data: ProductCreate) -> Product:
    try:
        specifications = product_data.specifications
        if not isinstance(specifications, dict):
            specifications = {}

        specifications_json = json.dumps(specifications, ensure_ascii=False) if specifications else None
        images_json = json.dumps(product_data.images or [], ensure_ascii=False)
        
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=Decimal(str(product_data.price)),
            category_id=product_data.category_id,
            images=images_json,
            specifications=specifications_json
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        return product
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка создания продукта: {str(e)}")

# Функция для обновления данных продукта по id
def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Product:
    try:
        product = get_product_by_id(db, product_id)
        
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден")

        data = product_data.model_dump(exclude_unset=True)
        
        for k, v in data.items():
            if k == "price" and v is not None:
                setattr(product, k, Decimal(v))
            elif k == "specifications" and v is not None:
                setattr(product, k, json.dumps(v, ensure_ascii=False))
            elif k == "images" and v is not None:
                setattr(product, k, json.dumps(v, ensure_ascii=False))
            elif v is not None:
                setattr(product, k, v)
        
        db.commit()
        db.refresh(product)
        
        return product
    
    except HTTPException:
        db.rollback()
        raise
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Функция для удаления продукта по id
def delete_product(db: Session, product_id: int):
    try:
        product = get_product_by_id(db, product_id)
        
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден")
        
        db.delete(product)
        db.commit()
        
        return
    
    except HTTPException:
        db.rollback()
        raise
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
