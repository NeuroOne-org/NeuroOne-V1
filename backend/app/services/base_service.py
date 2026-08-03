"""Shared service-layer infrastructure."""

from typing import Generic, TypeVar


RepositoryType = TypeVar("RepositoryType")


class BaseService(Generic[RepositoryType]):
    """Base service providing access to the repository."""

    def __init__(self, repository: RepositoryType):
        self.repository = repository
