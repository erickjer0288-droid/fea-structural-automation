# Advanced O-ring squeeze case study

This reproducible portfolio example combines deterministic screening, visual sensitivity analysis, cross-section comparison, hardness mapping, and Monte Carlo tolerance simulation.

## Engineering question

How does a target MMC squeeze limit affect the nominal operating point, estimated line load, tolerance risk, and sensitivity to groove depth?

## Illustrative inputs

- Cross-section: 1.78 mm
- Hardness: 80 Shore A
- Baseline squeeze: LMC 18%, nominal 25%, MMC 33%
- Target MMC squeeze: 30%
- Groove sensitivity: 0.021 mm per percentage point
- Monte Carlo standard deviation: 2 percentage points
- Monte Carlo samples: 20,000
- Random seed: 42

All force curves and study values are generic portfolio data. They are not approved supplier data and must not be used for production release.

## Generated figures

1. Squeeze-load response by hardness.
2. Before/after operating-window comparison.
3. Groove-depth sensitivity for LMC, nominal, and MMC.
4. Hardness-squeeze heatmap of estimated line load.
5. Cross-section comparison at 80 Shore A.
6. Monte Carlo squeeze distribution with P05, P50, P95, and the upper limit.

## Reproduce the study

```bash
pip install -e .
python examples/advanced_case_study.py
```

The script writes PNG figures to `results/advanced_case_study/` and prints the estimated probability of exceeding the 30% squeeze limit.

## Interpretation boundaries

The model omits friction, temperature, aging, compression set, nonlinear material calibration, assembly effects, and detailed contact mechanics. The Monte Carlo model assumes a normal squeeze distribution for demonstration only. Real design decisions require traceable distributions, supplier data, testing, and detailed analysis.
