from fastapi import FastAPI
from app.api.main import api_router
from app.api.mainv2 import api_router as api_router_v2
from app.core.config import settings
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schema.response import Response
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=Response(
            status_code=exc.status_code,
            success=False,
            message=str(exc.detail),
            data=None
        ).model_dump()
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(api_router_v2, prefix=settings.API_V2_STR)
