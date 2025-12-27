from sqlalchemy.orm import Session
from typing import List, Optional
from models import Article
from schemas import ArticleCreate, ArticleUpdate
from fastapi import HTTPException, status
import json

def get_latest_articles(db: Session, limit: int = 4) -> List[Article]:
    try:
        return db.query(Article).order_by(Article.created_at.desc()).limit(limit).all()
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_article_by_id(db: Session, article_id: int) -> Optional[Article]:
    try:
        return db.query(Article).filter(Article.id == article_id).first()
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def create_article(db: Session, article_data: ArticleCreate, author_id: int) -> Article:
    try:
        images = article_data.images
        if images is not None:
            images = json.dumps(images, ensure_ascii=False)
        
        tags = article_data.tags
        if tags is not None:
            tags = json.dumps(tags, ensure_ascii=False)
        
        article = Article(
            name=article_data.name,
            short_description=article_data.short_description,
            content=article_data.content,
            images=images,
            tags=tags,
            author_id=author_id
        )
        
        db.add(article)
        db.commit()
        db.refresh(article)
        
        return article
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def update_article(db: Session, article_id: int, article_data: ArticleUpdate) -> Article:
    try:
        article = get_article_by_id(db, article_id)
        if not article:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Статья не найдена")
        
        data = article_data.model_dump(exclude_unset=True)
        
        for k, v in data.items():
            if k == "images" and v is not None:
                setattr(article, k, json.dumps(v, ensure_ascii=False))
            elif k == "tags" and v is not None:
                setattr(article, k, json.dumps(v, ensure_ascii=False))
            elif v is not None:
                setattr(article, k, v)
        
        db.commit()
        db.refresh(article)
        
        return article
    
    except HTTPException:
        db.rollback()
        raise
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def delete_article(db: Session, article_id: int):
    try:
        article = get_article_by_id(db, article_id)
        
        if not article:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Статья не найдена")
        
        db.delete(article)
        db.commit()
        
        return
    
    except HTTPException:
        db.rollback()
        raise
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
