from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from contextlib import asynccontextmanager, AsyncExitStack

from app.core.config import settings
from app.api.v1.api_routes import api_v1_router

# TODO: Import mcp server when needed
from app.mcp.sample_mcp.sample_server import sample_mcp_app
from app.mcp.animal_mcp.animal_server import animal_mcp_app

docs_url = None if settings.ENVIRONMENT == "production" else f"{settings.API_V1_STR}/docs"
redoc_url = None if settings.ENVIRONMENT == "production" else f"{settings.API_V1_STR}/redoc"
openapi_url = (
    None if settings.ENVIRONMENT == "production" else f"{settings.API_V1_STR}/openapi.json"
)

# Define a custom lifespan that uses only the necessary lifespan
@asynccontextmanager
async def combined_lifespan(app: FastAPI):
    print("Main app startup logic...")

    # Start the lifespan for the MCP server that requires it
    # Combine all existing lifespans here
    # Use 'async with' to correctly enter and exit the lifespan context
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(sample_mcp_app.lifespan(app))
        await stack.enter_async_context(animal_mcp_app.lifespan(app))
        # The 'yield' pauses the context manager, allowing the app to run
        yield

    print("Main app shutdown logic...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    default_response_class=UJSONResponse,
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
    lifespan=combined_lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: mount mcp server when needed

app.include_router(api_v1_router, prefix="/api/v1")
app.mount("/sample", sample_mcp_app)
app.mount("/animal", animal_mcp_app)
