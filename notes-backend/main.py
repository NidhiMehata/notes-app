import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from config import settings
from database.database import get_db
from exceptions import NoteNotFoundError, UserNotFoundError
from logging_config import setup_logging
from routers import auth, notes, users

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(users.router)
app.include_router(notes.router)
app.include_router(auth.router)


@app.exception_handler(NoteNotFoundError)
@app.exception_handler(UserNotFoundError)
def not_found_exception_handler(
    request: Request,
    exc: NoteNotFoundError | UserNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception("Unhandled exception")

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/healthz")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "message": "Notes API is running"}


app = CORSMiddleware(
    app,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
