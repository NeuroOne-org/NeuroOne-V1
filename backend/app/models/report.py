from base import BaseModel


"""
+----------------------+
|      REPORT          |
+----------------------+
| PK id                |
| FK diagnosis_id      |
| pdf_path             |
| summary              |
| recommendations      |
| generated_at         |
+----------------------+
"""

class Report(BaseModel):
    """Report model definitions."""
    pass
