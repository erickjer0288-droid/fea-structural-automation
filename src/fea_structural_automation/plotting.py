"""Publication-ready plots for the sanitized O-ring case study."""

from collections.abc import Iterable
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .curves import AVAILABLE_CROSS_SECTIONS_IN
from .squeeze import estimate_line_load
from .uncertainty import MonteCarloResult
from .units import lbf_per_in_to_n_per_mm


def _finish(path: Path, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def plot_squeeze_load_by_hardness(path: Path, cross_section_in: float = 0.070) -> None:
    """Plot estimated line load versus squeeze for several hardness values."""
    squeeze = np.linspace(5.0, 30.0, 101)
    for shore in (70.0, 80.0, 90.0):
        loads = [
            lbf_per_in_to_n_per_mm(estimate_line_load(cross_section_in, shore, x)[0])
            for x in squeeze
        ]
        plt.plot(squeeze, loads, label=f"Shore {shore:.0f}A")
    plt.xlabel("Squeeze [%]")
    plt.ylabel("Estimated line load [N/mm]")
    plt.grid(True, alpha=0.3)
    plt.legend()
    _finish(path, "Squeeze-load response by hardness")


def plot_operating_window(
    path: Path,
    before: tuple[float, float, float],
    after: tuple[float, float, float],
    upper_limit: float,
) -> None:
    """Compare baseline and updated LMC, nominal, and MMC squeeze states."""
    labels = ("LMC", "Nominal", "MMC")
    x = np.arange(len(labels))
    width = 0.36
    plt.bar(x - width / 2, before, width, label="Before")
    plt.bar(x + width / 2, after, width, label="After")
    plt.axhline(upper_limit, linestyle="--", label="Upper limit")
    plt.xticks(x, labels)
    plt.ylabel("Squeeze [%]")
    plt.legend()
    _finish(path, "Tolerance-window comparison")


def plot_groove_sensitivity(
    path: Path,
    baseline: tuple[float, float, float],
    mm_per_percent: float,
) -> None:
    """Plot squeeze-state sensitivity to groove-depth adjustment."""
    adjustment = np.linspace(-0.10, 0.15, 121)
    for value, label in zip(baseline, ("LMC", "Nominal", "MMC"), strict=True):
        squeeze = value - adjustment / mm_per_percent
        plt.plot(adjustment, squeeze, label=label)
    plt.xlabel("Groove-depth adjustment [mm]")
    plt.ylabel("Squeeze [%]")
    plt.grid(True, alpha=0.3)
    plt.legend()
    _finish(path, "Sensitivity to groove depth")


def plot_hardness_heatmap(path: Path, cross_section_in: float = 0.070) -> None:
    """Create a hardness-squeeze heatmap of estimated line load."""
    squeeze = np.linspace(5.0, 30.0, 51)
    hardness = np.linspace(70.0, 90.0, 41)
    values = np.array(
        [
            [
                lbf_per_in_to_n_per_mm(estimate_line_load(cross_section_in, shore, x)[0])
                for x in squeeze
            ]
            for shore in hardness
        ]
    )
    image = plt.imshow(
        values,
        origin="lower",
        aspect="auto",
        extent=(squeeze.min(), squeeze.max(), hardness.min(), hardness.max()),
    )
    plt.colorbar(image, label="Estimated line load [N/mm]")
    plt.xlabel("Squeeze [%]")
    plt.ylabel("Hardness [Shore A]")
    _finish(path, "Hardness-squeeze response map")


def plot_cross_section_comparison(
    path: Path,
    shore_a: float = 80.0,
    sections: Iterable[float] = AVAILABLE_CROSS_SECTIONS_IN,
) -> None:
    """Compare squeeze-load curves for all illustrative cross-sections."""
    squeeze = np.linspace(5.0, 30.0, 101)
    for section in sections:
        loads = [
            lbf_per_in_to_n_per_mm(estimate_line_load(section, shore_a, x)[0])
            for x in squeeze
        ]
        plt.plot(squeeze, loads, label=f"{section:.3f} in")
    plt.xlabel("Squeeze [%]")
    plt.ylabel("Estimated line load [N/mm]")
    plt.grid(True, alpha=0.3)
    plt.legend()
    _finish(path, f"Cross-section comparison at Shore {shore_a:.0f}A")


def plot_monte_carlo(
    path: Path,
    result: MonteCarloResult,
    upper_limit_percent: float,
) -> None:
    """Plot a Monte Carlo squeeze distribution and engineering limit."""
    plt.hist(result.squeeze_percent, bins=60, density=True, alpha=0.8)
    plt.axvline(result.p05_percent, linestyle="--", label="P05")
    plt.axvline(result.p50_percent, linestyle="-", label="P50")
    plt.axvline(result.p95_percent, linestyle="--", label="P95")
    plt.axvline(upper_limit_percent, linestyle=":", label="Upper limit")
    plt.xlabel("Squeeze [%]")
    plt.ylabel("Probability density")
    plt.legend()
    _finish(path, "Monte Carlo tolerance distribution")
