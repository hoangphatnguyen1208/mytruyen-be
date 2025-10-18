from starlette.middleware.base import BaseHTTPMiddleware
from app.schema.response import Response

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return Response(
                status_code=500,
                message="An internal server error occurred.",
                success=False,
            ).model_dump()
