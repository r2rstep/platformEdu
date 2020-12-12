from datetime import datetime


def create_slug(title: str) -> str:
    return '-'.join(title.lower().split())


def get_upload_time() -> datetime:
    return datetime.utcnow()
