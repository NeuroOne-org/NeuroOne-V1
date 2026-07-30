from base import BaseModel


"""
+----------------------+
|     RAG_SOURCE       |
+----------------------+
| PK id                |
| FK report_id         |
| title                |
| source_url           |
| citation             |
| chunk_id             |
+----------------------+
"""

class Rag(BaseModel):
    """Rag model definitions."""
    __tablename__ = "Rag"
    pass