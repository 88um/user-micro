import os
from functools import wraps
from fastapi import APIRouter, Depends, Form, Request
from pydantic import BaseModel
from database.engine import get_db, Session
from database.models import User
from instagrapi import Client
from dotenv import load_dotenv
load_dotenv()

session = os.getenv('sessionid')
proxy = os.getenv('proxy')
c = Client(proxy=proxy)
if session:
    try:
        c.login_by_sessionid(session)
    except Exception as e:
        print(e)

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

valid_ips = ["127.0.0.1","216.82.28.90"]

def auth(func):
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        print(request.client.host)
        if request.client.host in valid_ips:
            return await func(*args ,**kwargs)
        return {'Unauthorized': True}
    return wrapper


@router.get("/info")
@auth
async def user_info(
                    username: str , 
                    db : Session = Depends(get_db)):
    """Get user object from user id
    """
    user = db.query(User).filter(User.username == username.lower()).first()
    if user:
        return {"user_id": user.user_id}
    else:
        user_id = c.user_id_from_username(username)
        new_user = User(username=username, user_id=user_id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {'user_id': user_id}


@router.post("/add")
@auth
async def user_info(
                    username: str = Form(...), 
                    user_id : str = Form(...),
                    db : Session = Depends(get_db)):
    """Add user object to db
    """
    new_user = User(username=username, user_id=user_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user