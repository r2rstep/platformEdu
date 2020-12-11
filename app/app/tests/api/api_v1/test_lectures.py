from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.lecture import create_random_lecture


def test_create_lecture(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/lectures/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_get_lecture(
    client: TestClient, db: Session
) -> None:
    lecture = create_random_lecture(db)
    response = client.get(
        f"{settings.API_V1_STR}/lectures/{lecture.id}"
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == lecture.title
    assert content["content"] == lecture.content
    assert content["id"] == str(lecture.id)
    assert content["author_id"] == str(lecture.author_id)
