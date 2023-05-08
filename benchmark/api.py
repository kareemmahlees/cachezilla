# pylint: disable=import-error
import uvicorn
from db import Post, get_session
from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from cachezilla import CacheZilla

app = FastAPI()
cache = CacheZilla()


@app.get("/without", response_model=Post)
async def without_cache(session: Session = Depends(get_session)):
    return session.exec(select(Post).where(Post.id == 1)).first()


@app.get("/with/{post_id}", response_model=Post)
async def with_cache(post_id: int, session: Session = Depends(get_session)):
    post = cache.get(post_id)
    if post is None:
        post = session.exec(select(Post).where(Post.id == 1)).first()
        cache.set(post.id, post)
        return post
    return post


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)
