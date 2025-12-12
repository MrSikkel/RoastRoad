from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from schemas import ProductOut, ProductCreate, ProductUpdate
from crud.products import get_products, get_product_by_id, create_product, update_product, delete_product
from auth import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

# Эндпоинт для получения продуктов
@router.get("", response_model=List[ProductOut])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
    ):
    
    try:
        products = get_products(db, skip=skip, limit=limit)
        
        return products
    
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Эндпоинт для получения продукта по id
@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = get_product_by_id(db, product_id)
        
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден")
        
        return product
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Эндпоинт для создания нового продукта
@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_new_product(
    product_data: ProductCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    try:
        new_product = create_product(db, product_data)
    
        return new_product
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Эндпоинт для обновления продукта по id
@router.put("/{product_id}", response_model=ProductOut)
def update__product(
    product_id: int, 
    product_data: ProductUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    try:
        updated_product = update_product(db, product_id, product_data)
        
        return updated_product
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Эндпоинт для удаления продукта по id
@router.delete("/{product_id}")
def remove_product(
    product_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    try:
        delete_product(db, product_id)
        
        return {"message": "Продукт удалён"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
