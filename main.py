from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, create_engine, SQLModel
from fastapi_htmx.htmx import htmx, htmx_init

from routes import signup, login

app = FastAPI()
htmx_init(templates=Jinja2Templates('templates'))

app.include_router(signup.router)
app.include_router(login.router)

def get_session() -> Session:
    engine = create_engine('sqlite:///database.sqlite')
    SQLModel.metadata.create_all(engine)
    return Session(engine)

@app.get('/', response_class=HTMLResponse)
@htmx("index", 'index')
async def index(request:Request):
    sess = get_session()
    return {}
    
