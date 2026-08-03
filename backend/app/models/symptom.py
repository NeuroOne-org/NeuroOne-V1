from base import BaseModel


"""
+---------------------+
|      SYMPTOM        |
+---------------------+
| PK id               |
| FK visit_id         |
| symptom_name        |
| severity            |
| duration            |
| onset               |
+---------------------+
"""

class Symptom(BaseModel):
    """Symptom model definitions."""
    pass