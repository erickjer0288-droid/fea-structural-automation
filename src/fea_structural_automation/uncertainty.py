"""Reproducible tolerance and uncertainty analysis utilities."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True, slots=True)
class MonteCarloResult:
    """Summary and raw samples from a squeeze tolerance simulation."""

    squeeze_percent: NDArray[np.float64]
    mean_percent: float
    std_percent: float
    p05_percent: float
    p50_percent: float
    p95_percent: float
    probability_above_limit: float


def simulate_squeeze_tolerance(
    nominal_percent: float,
    sigma_percent: float,
    upper_limit_percent: float,
    samples: int = 20_000,
    seed: int = 42,
) -> MonteCarloResult:
    """Run a seeded normal-distribution Monte Carlo squeeze study."""
    if sigma_percent <= 0:
        raise ValueError("sigma_percent must be greater than zero")
    if samples < 100:
        raise ValueError("samples must be at least 100")

    rng = np.random.default_rng(seed)
    values = rng.normal(nominal_percent, sigma_percent, samples).astype(np.float64)
    values = np.clip(values, 0.0, None)

    return MonteCarloResult(
        squeeze_percent=values,
        mean_percent=float(np.mean(values)),
        std_percent=float(np.std(values, ddof=1)),
        p05_percent=float(np.percentile(values, 5)),
        p50_percent=float(np.percentile(values, 50)),
        p95_percent=float(np.percentile(values, 95)),
        probability_above_limit=float(np.mean(values > upper_limit_percent)),
    )
