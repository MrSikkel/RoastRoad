from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from schemas import ArticleOut, ArticleCreate, ArticleUpdate
from crud.articles import get_latest_articles, get_article_by_id, create_article, update_article, delete_article
from auth import get_current_user

router = APIRouter(prefix="/articles", tags=["articles"])

@router.get("", response_model=List[ArticleOut])
def list_latest_articles(db: Session = Depends(get_db)):
    try:
        articles = get_latest_articles(db, limit=4)
        
        return articles
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{article_id}", response_model=ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    try:
        article = get_article_by_id(db, article_id)
        
        if not article:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Статья не найдена")
        
        return article
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("", response_model=ArticleOut, status_code=status.HTTP_201_CREATED)
def create_new_article(
    article_data: ArticleCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    try:
        new_article = create_article(db, article_data, current_user.id)
        
        return new_article
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{article_id}", response_model=ArticleOut)
def update__article(
    article_id: int, 
    article_data: ArticleUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    try:
        updated_article = update_article(db, article_id, article_data)
        
        return updated_article
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{article_id}")
def remove_article(
    article_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    try:
        delete_article(db, article_id)
        
        return {"message": "Статья удалена"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
