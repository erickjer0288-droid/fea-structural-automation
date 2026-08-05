"""Generate the complete advanced visual O-ring case study."""

from pathlib import Path

from fea_structural_automation.models import OringStudy, SqueezeState
from fea_structural_automation.plotting import (
    plot_cross_section_comparison,
    plot_groove_sensitivity,
    plot_hardness_heatmap,
    plot_monte_carlo,
    plot_operating_window,
    plot_squeeze_load_by_hardness,
)
from fea_structural_automation.squeeze import evaluate_oring_study
from fea_structural_automation.uncertainty import simulate_squeeze_tolerance

OUTPUT = Path("results/advanced_case_study")
BASELINE = SqueezeState(18.0, 25.0, 33.0)
STUDY = OringStudy(
    cross_section_mm=1.78,
    shore_a=80.0,
    target_mmc_percent=30.0,
    baseline=BASELINE,
)

result = evaluate_oring_study(STUDY)
monte_carlo = simulate_squeeze_tolerance(
    nominal_percent=result.squeeze.nominal_percent,
    sigma_percent=2.0,
    upper_limit_percent=30.0,
    samples=20_000,
    seed=42,
)

plot_squeeze_load_by_hardness(OUTPUT / "01_squeeze_load_by_hardness.png")
plot_operating_window(
    OUTPUT / "02_operating_window.png",
    (BASELINE.lmc_percent, BASELINE.nominal_percent, BASELINE.mmc_percent),
    (
        result.squeeze.lmc_percent,
        result.squeeze.nominal_percent,
        result.squeeze.mmc_percent,
    ),
    upper_limit=30.0,
)
plot_groove_sensitivity(
    OUTPUT / "03_groove_sensitivity.png",
    (BASELINE.lmc_percent, BASELINE.nominal_percent, BASELINE.mmc_percent),
    STUDY.mm_per_percent,
)
plot_hardness_heatmap(OUTPUT / "04_hardness_heatmap.png")
plot_cross_section_comparison(OUTPUT / "05_cross_section_comparison.png")
plot_monte_carlo(OUTPUT / "06_monte_carlo.png", monte_carlo, upper_limit_percent=30.0)

print(f"Generated case-study figures in {OUTPUT.resolve()}")
print(f"Estimated probability above 30% squeeze: {monte_carlo.probability_above_limit:.2%}")
