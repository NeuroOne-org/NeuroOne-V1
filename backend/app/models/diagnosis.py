from base import BaseModel

"""
+----------------------+    
|     DIAGNOSIS        |    
+----------------------+    
| PK id                |    
| FK visit_id          |    
| ai_prediction        |    
| confidence_score     |    
| explanation          |    
| final_diagnosis      |    
| doctor_verified      |    
| created_at           |
+----------------------+
"""

class Diagnosis(BaseModel):
    """Diagnosis model definitions."""
    pass