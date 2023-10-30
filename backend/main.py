import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api import postcard_api_router


origins = [
    #  "http://localhost:5173",
    "*",
]


app = FastAPI(
    title="FastAPI postcard constructor",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_api_router = APIRouter()

main_api_router.include_router(
    postcard_api_router,
    prefix="/postcards",
    tags=["postcards"]
)


app.include_router(
    main_api_router,
    prefix="/api"
)


if __name__ == '__main__':
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8888,
    )
