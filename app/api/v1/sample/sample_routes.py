from fastapi import APIRouter


sample_router = APIRouter(tags=["sample"])


@sample_router.get("/hello")
async def say_hello():
    return dict(
        message='ok',
        payload="Hello, World!"
    )
