from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.channels.router import router as youtube_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(youtube_router, prefix="/api/youtube")
