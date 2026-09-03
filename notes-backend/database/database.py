import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

logger = logging.getLogger(__name__)


def create_db_engine(database_url: str):
    return create_engine(database_url)


engine = create_db_engine(settings.database_url)


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    except Exception:
        logger.exception("Database transaction failed")
        db.rollback()
        raise
    else:
        db.commit()
    finally:
        db.close()
