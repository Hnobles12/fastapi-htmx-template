from fastapi_htmx import htmx
from dataclasses import dataclass
from fastapi import Form, Request, Response, APIRouter
from fastapi.responses import HTMLResponse
from typing import Annotated
from sqlmodel import select, Session

from .models.users import User, UserCreds
from .utils import get_session

router = APIRouter(prefix="/login", tags=['login'])

@router.get('/', response_class=HTMLResponse)
@htmx("login","login")
async def get_login_form(request:Request, response:Response):
    return {}
    
@router.post('/submit')
async def login(request:Request, response:Response, username:Annotated[str, Form()], password:Annotated[str,Form()]):
    #user = User(username=username, password=password)
    session = get_session()
    user = session.exec(select(User).where(User.username == username and User.password == password)).one()
    creds:UserCreds = session.exec(select(UserCreds).where(UserCreds.username == username)).one()

    valid_login = creds.login()
    if valid_login:
        creds.renew_session()
        response.headers["HX-Redirect"] = '/'
        return {}
    
    else:
        return {}


    print(f'User is: {user.username}')

    if creds.login(password):
        print("Password Matched.")
    else:
        print("Passwords did not match.")


    return {}

