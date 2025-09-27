import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def _test_db_path(tmp_path_factory):
    base = tmp_path_factory.mktemp("db")
    db_file = base / "test.db"
    return db_file


@pytest.fixture(scope="session")
def app_instance(_test_db_path):
    db_url = f"sqlite:///{_test_db_path.as_posix()}?check_same_thread=false"
    os.environ["DATABASE_URL"] = db_url
    from app.main import app

    return app


@pytest.fixture()
def client(app_instance):
    return TestClient(app_instance)


@pytest.fixture(autouse=True)
def db_reset():
    from app.db.session import engine
    from app.db.base import Base

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

