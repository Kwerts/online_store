import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routers import router
from database.models import create_database_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://188.225.26.157",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"], 
)

app.include_router(router=router)


# For deploying
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)