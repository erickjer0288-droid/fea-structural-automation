import pytest

from fea_structural_automation import OringStudy, evaluate_oring_study
from fea_structural_automation.interpolation import interpolate_curve, linear_interpolate


def test_linear_interpolation_midpoint() -> None:
    assert linear_interpolate(5.0, 0.0, 0.0, 10.0, 20.0) == pytest.approx(10.0)


def test_curve_lookup_clamps_outside_domain() -> None:
    value, effective_x, was_clamped = interpolate_curve({5: 2.0, 10: 6.0}, 2.0)
    assert value == pytest.approx(2.0)
    assert effective_x == pytest.approx(5.0)
    assert was_clamped is True


def test_default_study_reduces_squeeze_from_mmc_target() -> None:
    result = evaluate_oring_study(
        OringStudy(cross_section_mm=1.78, shore_a=80.0, target_mmc_percent=30.0)
    )
    assert result.reduction_percentage_points == pytest.approx(3.0)
    assert result.groove_depth_adjustment_mm == pytest.approx(0.063)
    assert result.squeeze.lmc_percent == pytest.approx(15.0)
    assert result.squeeze.nominal_percent == pytest.approx(22.0)
    assert result.squeeze.mmc_percent == pytest.approx(30.0)
    assert result.nominal_line_load_lbf_per_in > 0.0
    assert result.nominal_line_load_n_per_mm > 0.0


def test_target_above_baseline_does_not_create_negative_adjustment() -> None:
    result = evaluate_oring_study(
        OringStudy(cross_section_mm=2.62, shore_a=75.0, target_mmc_percent=35.0)
    )
    assert result.reduction_percentage_points == 0.0
    assert result.groove_depth_adjustment_mm == 0.0
    assert result.squeeze.nominal_percent == 25.0
    assert result.squeeze.mmc_percent == 35.0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("cross_section_mm", 0.0),
        ("shore_a", 0.0),
        ("target_mmc_percent", -1.0),
        ("mm_per_percent", 0.0),
    ],
)
def test_invalid_inputs_raise_value_error(field: str, value: float) -> None:
    kwargs = {
        "cross_section_mm": 1.78,
        "shore_a": 80.0,
        "target_mmc_percent": 30.0,
        "mm_per_percent": 0.021,
    }
    kwargs[field] = value
    with pytest.raises(ValueError):
        evaluate_oring_study(OringStudy(**kwargs))
