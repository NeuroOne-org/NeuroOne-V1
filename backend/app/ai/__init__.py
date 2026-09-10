"""AI orchestration.

Layering rule: nothing in this package imports a repository or touches a
database Session. The pipeline accepts a ClinicalContext and returns an
AnalysisResult; persistence belongs to the service layer (ADR-003).
"""

from .context import build_clinical_context
from .orchestrator import AnalysisOrchestrator
from .providers import build_providers
from .trends import detect_trends

__all__ = [
    "AnalysisOrchestrator",
    "build_clinical_context",
    "build_providers",
    "detect_trends",
]
