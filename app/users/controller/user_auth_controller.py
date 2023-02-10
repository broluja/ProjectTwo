from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.users.service import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, role: list, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.role = role

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            payload = self.verify_jwt(credentials.credentials)
            if not payload.get("valid"):
                raise HTTPException(status_code=403, detail="Invalid or expired token.")
            if payload.get("role") not in self.role:
                raise HTTPException(status_code=403, detail="You have no permission to access this route.")
            return credentials.credentials

        raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(jwt_token: str) -> dict:
        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            print(e)
            payload = None
        return {"valid": bool(payload), "role": payload["role"] if payload else None}
