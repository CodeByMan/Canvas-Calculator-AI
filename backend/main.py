from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from constants import ENV, FRONTEND_ORIGINS, PORT, SERVER_URL
from src.calculator.route import router as calculator_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/")
async def check_status():
    return {"status": "ok"}


app.include_router(calculator_router, prefix="/api/calculate-results", tags=["calculate"])


if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVER_URL, port=int(PORT), reload=(ENV == "dev"))
