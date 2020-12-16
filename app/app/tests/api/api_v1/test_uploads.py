from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.core.config import settings
from app import crud


@pytest.fixture(autouse=True, scope='module')
def test_setup(db: Session):
    yield
    crud.job.remove_all(db)


def test_uploads(client: TestClient):
    resp = client.post(f'{settings.API_V1_STR}/batchUpload')
    assert resp.status_code == 303
    assert resp.headers["Location"].startswith(f'{settings.API_V1_STR}/jobs')
