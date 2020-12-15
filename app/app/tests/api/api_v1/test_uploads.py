from fastapi.testclient import TestClient

from app.core.config import settings


def test_uploads(client: TestClient):
    resp = client.post(f'{settings.API_V1_STR}/batchUpload')
    assert resp.status_code == 303
    assert resp.headers["Location"] == f'{settings.API_V1_STR}/jobs/job-id'
