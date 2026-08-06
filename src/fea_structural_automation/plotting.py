"""Publication-ready plots for the sanitized O-ring case study."""

from collections.abc import Iterable
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .curves import AVAILABLE_CROSS_SECTIONS_IN
from .squeeze import estimate_line_load
from .uncertainty import MonteCarloResult
from .units import lbf_per_in_to_n_per_mm


def _new_figure() -> None:
    """Create a consistent figure canvas for portfolio graphics."""
    plt.figure(figsize=(8.2, 5.2))
    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.titlesize": 15,
            "axes.labelsize": 12,
            "legend.fontsize": 10,
        }
    )


def _finish(path: Path, title: str, subtitle: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.title(title, fontweight="bold", pad=14)
    if subtitle:
        plt.gcf().text(0.5, 0.93, subtitle, ha="center", fontsize=9)
    plt.tight_layout(rect=(0.0, 0.0, 1.0, 0.92 if subtitle else 1.0))
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()


def plot_squeeze_load_by_hardness(path: Path, cross_section_in: float = 0.070) -> None:
    """Plot estimated line load versus squeeze for several hardness values."""
    _new_figure()
    squeeze = np.linspace(5.0, 30.0, 101)
    for shore in (70.0, 80.0, 90.0):
        loads = [
            lbf_per_in_to_n_per_mm(estimate_line_load(cross_section_in, shore, x)[0])
            for x in squeeze
        ]
        width = 2.8 if shore == 80.0 else 1.8
        plt.plot(squeeze, loads, linewidth=width, label=f"Shore {shore:.0f}A")
        marker_x = np.array([10.0, 20.0, 30.0])
        marker_y = [
            lbf_per_in_to_n_per_mm(estimate_line_load(cross_section_in, shore, x)[0])
            for x in marker_x
        ]
        plt.scatter(marker_x, marker_y, s=28)
    plt.xlabel("Squeeze [%]")
    plt.ylabel("Estimated line load [N/mm]")
    plt.grid(True, alpha=0.25)
    plt.legend(frameon=False)
    _finish(
        path,
        "Illustrative squeeze-load response by Shore hardness",
        "Highlighted curve: Shore 80A | Screening data only",
    )


def plot_operating_window(
    path: Path,
    before: tuple[float, float, float],
    after: tuple[float, float, float],
    upper_limit: float,
) -> None:
    """Compare baseline and updated LMC, nominal, and MMC squeeze states."""
    _new_figure()
    labels = ("LMC", "Nominal", "MMC")
    x = np.arange(len(labels))
    width = 0.36
    before_bars = plt.bar(x - width / 2, before, width, label="Before")
    after_bars = plt.bar(x + width / 2, after, width, label="After")
    plt.axhline(upper_limit, linestyle="--", linewidth=1.8, label="Target MMC limit")
    plt.text(
        len(labels) - 0.52,
        upper_limit + 0.45,
        f"Target = {upper_limit:.0f}%",
        ha="right",
        fontsize=10,
    )
    for bars in (before_bars, after_bars):
        for bar in bars:
            height = float(bar.get_height())
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.45,
                f"{height:.0f}%",
                ha="center",
                va="bottom",
                fontsize=10,
            )
    plt.xticks(x, labels)
    plt.ylabel("Squeeze [%]")
    plt.ylim(0.0, max(max(before), upper_limit) + 5.0)
    plt.grid(axis="y", alpha=0.2)
    plt.legend(frameon=False)
    _finish(
        path,
        "Tolerance-window comparison",
        "Design update moves the MMC condition to the selected upper target",
    )


def plot_groove_sensitivity(
    path: Path,
    baseline: tuple[float, float, float],
    mm_per_percent: float,
    target_mmc_percent: float = 30.0,
) -> None:
    """Plot squeeze-state sensitivity to groove-depth adjustment."""
    _new_figure()
    adjustment = np.linspace(-0.10, 0.15, 121)
    for value, label in zip(baseline, ("LMC", "Nominal", "MMC"), strict=True):
        squeeze = value - adjustment / mm_per_percent
        plt.plot(adjustment, squeeze, linewidth=2.0, label=label)

    selected_adjustment = (baseline[2] - target_mmc_percent) * mm_per_percent
    plt.axvline(selected_adjustment, linestyle="--", linewidth=1.8)
    plt.axhline(target_mmc_percent, linestyle=":", linewidth=1.5)
    plt.scatter([selected_adjustment], [target_mmc_percent], s=75, zorder=5)
    plt.annotate(
        f"Selected adjustment\n{selected_adjustment:.3f} mm",
        xy=(selected_adjustment, target_mmc_percent),
        xytext=(selected_adjustment + 0.025, target_mmc_percent + 4.0),
        arrowprops={"arrowstyle": "->"},
        fontsize=10,
    )
    plt.xlabel("Groove-depth adjustment [mm]")
    plt.ylabel("Squeeze [%]")
    plt.grid(True, alpha=0.25)
    plt.legend(frameon=False)
    _finish(
        path,
        "Sensitivity of squeeze to groove-depth adjustment",
        "Positive adjustment reduces LMC, nominal, and MMC squeeze",
    )


def plot_hardness_heatmap(path: Path, cross_section_in: float = 0.070) -> None:
    """Create a hardness-squeeze heatmap of estimated line load."""
    _new_figure()
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
    contours = plt.contour(squeeze, hardness, values, levels=5, linewidths=0.8)
    plt.clabel(contours, inline=True, fontsize=8, fmt="%.1f")
    colorbar = plt.colorbar(image)
    colorbar.set_label("Estimated line load [N/mm]", fontsize=11)
    plt.scatter([22.0], [80.0], s=75, marker="x", linewidths=2.2)
    plt.annotate("Nominal design point", xy=(22.0, 80.0), xytext=(14.5, 83.5))
    plt.xlabel("Squeeze [%]")
    plt.ylabel("Hardness [Shore A]")
    _finish(
        path,
        "Hardness-squeeze response map",
        "Contour labels indicate estimated line load in N/mm",
    )


def plot_cross_section_comparison(
    path: Path,
    shore_a: float = 80.0,
    sections: Iterable[float] = AVAILABLE_CROSS_SECTIONS_IN,
) -> None:
    """Compare squeeze-load curves for all illustrative cross-sections."""
    _new_figure()
    squeeze = np.linspace(5.0, 30.0, 101)
    for section in sections:
        loads = [
            lbf_per_in_to_n_per_mm(estimate_line_load(section, shore_a, x)[0])
            for x in squeeze
        ]
        section_mm = section * 25.4
        plt.plot(
            squeeze,
            loads,
            linewidth=2.0,
            label=f"{section:.3f} in ({section_mm:.2f} mm)",
        )
    plt.xlabel("Squeeze [%]")
    plt.ylabel("Estimated line load [N/mm]")
    plt.grid(True, alpha=0.25)
    plt.legend(frameon=False, ncol=2)
    _finish(
        path,
        f"Cross-section comparison at Shore {shore_a:.0f}A",
        "Larger cross-sections produce higher estimated line load",
    )


def plot_monte_carlo(
    path: Path,
    result: MonteCarloResult,
    upper_limit_percent: float,
) -> None:
    """Plot a Monte Carlo squeeze distribution and engineering limit."""
    _new_figure()
    plt.hist(result.squeeze_percent, bins=60, density=True, alpha=0.78)
    plt.axvspan(upper_limit_percent, result.squeeze_percent.max(), alpha=0.18)
    plt.axvline(result.p05_percent, linestyle="--", linewidth=1.5, label="P05")
    plt.axvline(result.p50_percent, linestyle="-", linewidth=2.0, label="P50")
    plt.axvline(result.p95_percent, linestyle="--", linewidth=1.5, label="P95")
    plt.axvline(upper_limit_percent, linestyle=":", linewidth=2.0, label="Upper limit")
    summary = (
        f"Samples: {result.squeeze_percent.size:,}\n"
        f"Seed: 42\n"
        f"P(> {upper_limit_percent:.0f}%) = "
        f"{result.probability_above_limit:.3%}"
    )
    plt.text(
        0.98,
        0.96,
        summary,
        transform=plt.gca().transAxes,
        ha="right",
        va="top",
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.9},
        fontsize=10,
    )
    plt.xlabel("Squeeze [%]")
    plt.ylabel("Probability density")
    plt.grid(axis="y", alpha=0.2)
    plt.legend(frameon=False, loc="upper left")
    _finish(
        path,
        "Monte Carlo tolerance distribution",
        "Illustrative normal-distribution model with deterministic random seed",
    )
