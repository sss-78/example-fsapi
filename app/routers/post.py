from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(limit)
    # cursor.execute(f'select * from posts')
    # posts = cursor.fetchall()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()
    # print(results)
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
     # cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning *""", 
    # (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **(post.dict()))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts where id = (%s)""", (str(id)))
    # test_post = cursor.fetchall()

    # test_post = db.query(models.Post).first()    

    test_post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    

    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post id: {id} not found")


    return test_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""delete from posts where id = (%s) returning * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} does not exist")
    
    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform action")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_posts(post: schemas.PostCreate, id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *""", 
    # (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post1 = updated_post.first()
    
    if not post1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} does not exist")
    
    if post1.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform action")
    
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()