"""Engineering unit conversions used by the screening package."""

LBF_PER_IN_TO_N_PER_MM = 4.4482216152605 / 25.4
MM_PER_IN = 25.4


def mm_to_in(value_mm: float) -> float:
    """Convert millimetres to inches."""
    return value_mm / MM_PER_IN


def lbf_per_in_to_n_per_mm(value: float) -> float:
    """Convert line load from lbf/in to N/mm."""
    return value * LBF_PER_IN_TO_N_PER_MM
