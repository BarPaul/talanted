from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("access_token")
        if token and not request.headers.get("authorization"):
            headers = dict(request.headers)
            headers["authorization"] = f"Bearer {token}"
            request = Request(request.scope, request.receive)
            request._headers = headers
            
        return await call_next(request)