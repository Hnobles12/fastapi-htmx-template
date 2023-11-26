from typing import Optional
from sqlmodel import Field, SQLModel
from hashlib import sha512
from secrets import token_hex, token_urlsafe
from datetime import datetime, timedelta

MAX_SESSION_LENGTH = timedelta(minutes=30)


class UserCreds(SQLModel, table=True):
    username: Optional[str] = Field(default=None, primary_key=True)
    salt: Optional[str] = None
    pass_hash: Optional[str] = None
    session_start: Optional[str] = None
    session_key: Optional[str] = None

    def generate_hash(self, password: str) -> None:
        if self.salt == None:
            self.salt = token_hex(16)
        pass_str = f"{password.encode('utf-8')}{self.salt}"
        hasher = sha512()
        hasher.update(password.encode('utf-8'))
        hasher.update(self.salt.encode('utf-8'))
        pass_hash = hasher.hexdigest()
        return pass_hash

    def login(self, password: str):
        hash = self.generate_hash(password)
        if hash == self.pass_hash:
            return True
        else:
            return False

    def renew_session(self, new_key=True) -> str:
        dt = datetime.now().isoformat()
        self.session_start = dt
        if new_key:
            self.session_key = token_urlsafe(16)
        return self.session_key

    def check_session_key(self, key: str, renew: bool = False) -> bool:
        if self.session_key == key:
            start = datetime.fromisoformat(self.session_start)
            now = datetime.now()
            delta = now-start
            if delta <= MAX_SESSION_LENGTH:
                if renew:
                    self.renew_session(new_key=False)
                return True
            else:
                return False
        else:
            return False


class User(SQLModel, table=True):
    username: Optional[str] = Field(default=None, primary_key=True)
    email: Optional[str] = None
    password: Optional[str] = None
