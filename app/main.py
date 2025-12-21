from fastapi import FastAPI
from app.api.main import api_router
from app.api.mainv2 import api_router as api_router_v2
from app.core.config import settings
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schema.response import Response
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import torch
from FlagEmbedding import BGEM3FlagModel
from pinecone import Pinecone
from contextlib import asynccontextmanager

device = torch.device("cpu")

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     app.state.search_model = BGEM3FlagModel('BAAI/bge-m3', device='cpu')
#     app.state.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
#     app.state.pc_index = app.state.pc.Index("hybrid-spilt")
#     yield
#     del app.state.search_model

app = FastAPI(
    title=settings.PROJECT_NAME,
    # lifespan=lifespan
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
