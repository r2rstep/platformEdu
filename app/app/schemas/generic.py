from typing import List, TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel


class PaginationLinks(BaseModel):
    self: str
    previous: str = None
    next: str = None


ElementType = TypeVar('ElementType')


class Elements(GenericModel, Generic[ElementType]):
    total: int
    count: int
    items: List[ElementType]
    links: PaginationLinks
