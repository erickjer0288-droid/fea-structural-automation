"""O-ring squeeze and line-load quick-screen calculations."""

from .curves import AVAILABLE_CROSS_SECTIONS_IN, ILLUSTRATIVE_LINE_LOAD_CURVES
from .interpolation import interpolate_curve, linear_interpolate
from .models import OringStudy, ScreeningResult, SqueezeState
from .units import lbf_per_in_to_n_per_mm, mm_to_in


def nearest_cross_section(cross_section_mm: float) -> tuple[float, bool]:
    """Select the nearest illustrative curve cross-section."""
    requested_in = mm_to_in(cross_section_mm)
    selected = min(AVAILABLE_CROSS_SECTIONS_IN, key=lambda value: abs(value - requested_in))
    return selected, abs(selected - requested_in) > 1e-12


def estimate_line_load(
    cross_section_in: float,
    shore_a: float,
    squeeze_percent: float,
) -> tuple[float, float, bool]:
    """Estimate line load from illustrative 70A and 90A screening curves."""
    try:
        curve_70 = ILLUSTRATIVE_LINE_LOAD_CURVES[(cross_section_in, 70)]
        curve_90 = ILLUSTRATIVE_LINE_LOAD_CURVES[(cross_section_in, 90)]
    except KeyError as exc:
        raise ValueError("No illustrative curves exist for this cross-section") from exc

    load_70, effective_percent, clamped_70 = interpolate_curve(curve_70, squeeze_percent)
    load_90, effective_percent_90, clamped_90 = interpolate_curve(curve_90, squeeze_percent)
    if effective_percent != effective_percent_90:
        raise RuntimeError("Illustrative curves have inconsistent domains")

    line_load = linear_interpolate(shore_a, 70.0, load_70, 90.0, load_90)
    return line_load, effective_percent, clamped_70 or clamped_90


def evaluate_oring_study(study: OringStudy) -> ScreeningResult:
    """Evaluate an MMC-driven O-ring screening study.

    Reductions are applied only when the requested MMC target is lower than the
    baseline MMC value. This preserves the conservative intent of the original
    quick-screen workflow.
    """
    study.validate()

    reduction = max(0.0, study.baseline.mmc_percent - study.target_mmc_percent)
    squeeze = SqueezeState(
        lmc_percent=max(0.0, study.baseline.lmc_percent - reduction),
        nominal_percent=max(0.0, study.baseline.nominal_percent - reduction),
        mmc_percent=study.target_mmc_percent,
    )
    adjustment_mm = reduction * study.mm_per_percent

    selected_cross_section, approximated = nearest_cross_section(study.cross_section_mm)
    line_load_lbf_per_in, effective_percent, was_clamped = estimate_line_load(
        selected_cross_section,
        study.shore_a,
        squeeze.nominal_percent,
    )

    return ScreeningResult(
        squeeze=squeeze,
        groove_depth_adjustment_mm=adjustment_mm,
        reduction_percentage_points=reduction,
        selected_cross_section_in=selected_cross_section,
        nominal_line_load_lbf_per_in=line_load_lbf_per_in,
        nominal_line_load_n_per_mm=lbf_per_in_to_n_per_mm(line_load_lbf_per_in),
        force_lookup_percent=effective_percent,
        force_lookup_was_clamped=was_clamped,
        cross_section_was_approximated=approximated,
    )
