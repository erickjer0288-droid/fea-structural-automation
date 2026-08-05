"""Minimal API example for the sanitized O-ring quick-screen."""

from fea_structural_automation import (
    OringStudy,
    evaluate_oring_study,
)


study = OringStudy(
    cross_section_mm=1.78,
    shore_a=80.0,
    target_mmc_percent=30.0,
)
result = evaluate_oring_study(study)

print(result)
