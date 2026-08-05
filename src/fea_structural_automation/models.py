"""Typed input and output models for engineering screening studies."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SqueezeState:
    """LMC, nominal, and MMC squeeze values expressed as percentages."""

    lmc_percent: float
    nominal_percent: float
    mmc_percent: float


@dataclass(frozen=True, slots=True)
class OringStudy:
    """Inputs for a sanitized O-ring squeeze quick-screen study."""

    cross_section_mm: float
    shore_a: float
    target_mmc_percent: float
    mm_per_percent: float = 0.021
    baseline: SqueezeState = SqueezeState(18.0, 25.0, 33.0)

    def validate(self) -> None:
        """Validate basic physical and numerical constraints."""
        if self.cross_section_mm <= 0:
            raise ValueError("cross_section_mm must be greater than zero")
        if not 0 < self.shore_a <= 100:
            raise ValueError("shore_a must be in the interval (0, 100]")
        if self.target_mmc_percent < 0:
            raise ValueError("target_mmc_percent cannot be negative")
        if self.mm_per_percent <= 0:
            raise ValueError("mm_per_percent must be greater than zero")


@dataclass(frozen=True, slots=True)
class ScreeningResult:
    """Calculated quick-screen results and traceability metadata."""

    squeeze: SqueezeState
    groove_depth_adjustment_mm: float
    reduction_percentage_points: float
    selected_cross_section_in: float
    nominal_line_load_lbf_per_in: float
    nominal_line_load_n_per_mm: float
    force_lookup_percent: float
    force_lookup_was_clamped: bool
    cross_section_was_approximated: bool
