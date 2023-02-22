"""JWT class module"""
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.users.service import decode_jwt


class JWTBearer(HTTPBearer):
    """Class for creation and verification of tokens."""
    def __init__(self, role: list, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.role = role

    async def __call__(self, request: Request):
        """
        The __call__ function is called when the class instance is called.
        It returns a coroutine, which can be awaited to get the result of the call.
        The __call__ function must accept one argument: request, which contains all information about
        the HTTP request that triggered this function call.

        Param self: Access the attributes and methods of the class inside a method.
        Param request:Request: Get the authorization header from the request.
        Return: The token if the credentials are valid.
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
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
        """
        Function takes a JWT token as input and returns a dictionary with two keys:
        — valid: True if the token is valid, False otherwise.
        — role: The user's role (if any)

        Param jwt_token:str: Pass the jwt token to be verified
        Return: A dictionary with the key of 'valid' set to true if the jwt token is valid and false otherwise.
        """
        try:
            payload = decode_jwt(jwt_token)
        except Exception as exc:
            print(exc)
            payload = None
        return {"valid": bool(payload), "role": payload["role"] if payload else None}
