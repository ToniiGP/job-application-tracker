from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import os 
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
import jwt

SECRET_KEY = os.getenv("SECRET_KEY")

load_dotenv()

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the .env file.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hasher.verify(
        plain_password,
        hashed_password,
    )

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    payload = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    

def decode_access_token(
    token: str,
) -> dict:
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )