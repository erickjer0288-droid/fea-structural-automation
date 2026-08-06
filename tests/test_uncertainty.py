"""Tests for reproducible tolerance simulation."""

import pytest

from fea_structural_automation.uncertainty import simulate_squeeze_tolerance


def test_monte_carlo_is_reproducible() -> None:
    first = simulate_squeeze_tolerance(22.0, 2.0, 30.0, samples=2_000, seed=7)
    second = simulate_squeeze_tolerance(22.0, 2.0, 30.0, samples=2_000, seed=7)

    assert first.mean_percent == pytest.approx(second.mean_percent)
    assert first.p95_percent == pytest.approx(second.p95_percent)
    assert first.probability_above_limit == pytest.approx(second.probability_above_limit)


def test_monte_carlo_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        simulate_squeeze_tolerance(22.0, 0.0, 30.0)
    with pytest.raises(ValueError):
        simulate_squeeze_tolerance(22.0, 2.0, 30.0, samples=99)
