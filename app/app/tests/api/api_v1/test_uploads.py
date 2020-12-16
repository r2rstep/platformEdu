from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.core.config import settings
from app import crud


@pytest.fixture(autouse=True, scope='module')
def test_setup(db: Session):
    yield
    crud.job.remove_all(db)
