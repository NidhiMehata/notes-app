import os
import subprocess
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from config import settings
from database.database import get_db

TEST_DB_NAME = f"notes_test_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="session")
def test_database():
    url = make_url(settings.database_url)

    admin_url = url.set(database="postgres")
    test_url = url.set(database=TEST_DB_NAME)

    admin_engine = create_engine(
        admin_url,
        isolation_level="AUTOCOMMIT",
    )

    try:
        with admin_engine.connect() as connection:
            connection.execute(text(f'CREATE DATABASE "{TEST_DB_NAME}"'))
    finally:
        admin_engine.dispose()

    os.environ["DATABASE_URL"] = test_url.render_as_string(hide_password=False)

    subprocess.run(
        ["python", "-m", "alembic", "upgrade", "head"],
        check=True,
    )

    yield test_url

    admin_engine = create_engine(
        admin_url,
        isolation_level="AUTOCOMMIT",
    )

    try:
        with admin_engine.connect() as connection:
            connection.execute(
                text(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}" WITH (FORCE)')
            )
    finally:
        admin_engine.dispose()


@pytest.fixture
def db_session(test_database):
    engine = create_engine(test_database)

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    db = SessionLocal()

    try:
        yield db
    finally:
        db.rollback()
        db.close()
        engine.dispose()


@pytest.fixture
def client(test_database, db_session):
    from main import app

    fastapi_app = app.app

    def override_get_db():
        try:
            yield db_session
        except Exception:
            db_session.rollback()
            raise
        else:
            db_session.commit()

    fastapi_app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    fastapi_app.dependency_overrides.clear()
