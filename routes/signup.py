from fastapi_htmx import htmx
from dataclasses import dataclass
from fastapi import Form, Request, Response, APIRouter
from fastapi.responses import HTMLResponse
from typing import Annotated
from sqlmodel import select, SQLModel

from .models.users import User, UserCreds
from .utils import get_session

router = APIRouter(prefix="/signup", tags=['signup'])

@router.get('/', response_class=HTMLResponse)
@htmx("signup","signup")
async def get_signup_form(request:Request, response:Response):
    return {}
    
@router.post('/submit')
async def signup(request:Request, response:Response, username:Annotated[str, Form()], email:Annotated[str,Form()], password:Annotated[str,Form()]):
    user = User(username=username, password=password, email=email)

    session = get_session();
    st = select(User).where(User.username == username)
    users = session.exec(st).all()
    if len(users) != 0:
        print(f"User with username '{username}' exists")
        return {}
    else:
        session.add(User(username=username, email=email))
        session.commit()

        creds = UserCreds(username=username)
        creds.pass_hash = creds.generate_hash(password)
        
        session = get_session()
        session.add(creds)
        session.commit()


    return {
        "username":username,
        "email":email,
        "password":password,
    }


@router.post("/api/create_user")
async def create_user(request:Request, user: User):
    session = get_session()
    session.add(user)
    session.commit()
    return user