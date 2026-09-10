"""Helpers for consistent API responses."""

import math

from app.schemas.common import Pagination


def build_pagination(total: int, page: int, page_size: int) -> Pagination:
    """Build the pagination envelope shared by all collection endpoints."""

    total_pages = math.ceil(total / page_size) if page_size else 0
    return Pagination(
        page=page,
        page_size=page_size,
        total_records=total,
        total_pages=total_pages,
    )


__all__ = ["build_pagination"]
