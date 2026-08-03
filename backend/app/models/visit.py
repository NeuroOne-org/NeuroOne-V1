from base import BaseModel

"""
+----------------------+
|       VISIT          |
+----------------------+
| PK id                |
| FK patient_id        |
| visit_date           |
| chief_complaint      |
| history              |
| vitals               |
| notes                |
| status               |
| created_at           |
+----------------------+
"""
class Visit(BaseModel):
    pass
    """Visit model definitions."""
