from sqlmodel import create_engine, Session, SQLModel

def get_session() -> Session:
    engine = create_engine('sqlite:///database.sqlite')
    SQLModel.metadata.create_all(engine)
    return Session(engine)