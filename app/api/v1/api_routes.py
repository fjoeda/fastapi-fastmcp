from fastapi import APIRouter
from .sample.sample_routes import sample_router
from .mcpchat.mcp_chat_routes import mcp_client_routes


api_v1_router = APIRouter()
api_v1_router.include_router(sample_router, prefix="/sample")
api_v1_router.include_router(mcp_client_routes, prefix="/mcpchat")