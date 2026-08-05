"""Public API for FEA Structural Automation."""

from .models import OringStudy, ScreeningResult, SqueezeState
from .squeeze import evaluate_oring_study

__all__ = [
    "OringStudy",
    "ScreeningResult",
    "SqueezeState",
    "evaluate_oring_study",
]

__version__ = "0.1.0"
