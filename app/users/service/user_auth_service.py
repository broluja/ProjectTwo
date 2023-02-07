import time
from typing import Dict
import jwt

from app.config import settings
from app.users.exceptions import InvalidTokenException

USER_SECRET = settings.USER_SECRET
JWT_ALGORITHM = settings.ALGORYTHM


def sign_jwt(user_id: str, role: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "role": role,
        "expires": time.time() + 1200
    }
    token = jwt.encode(payload, USER_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token": token}


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, USER_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except (jwt.PyJWTError, jwt.InvalidTokenError):
        raise InvalidTokenException
