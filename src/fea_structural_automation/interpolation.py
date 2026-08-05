"""Small, dependency-free interpolation utilities."""

from collections.abc import Mapping


def linear_interpolate(x: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """Return the linear interpolation or extrapolation of *y* at *x*."""
    if x1 == x2:
        raise ValueError("Interpolation coordinates x1 and x2 must be different")
    fraction = (x - x1) / (x2 - x1)
    return y1 + fraction * (y2 - y1)


def interpolate_curve(curve: Mapping[int, float], x: float) -> tuple[float, float, bool]:
    """Interpolate a curve and clamp requests outside its domain.

    Returns the value, the effective lookup coordinate, and a clamp flag.
    """
    if len(curve) < 2:
        raise ValueError("A curve requires at least two points")

    coordinates = sorted(curve)
    effective_x = min(max(x, float(coordinates[0])), float(coordinates[-1]))
    was_clamped = effective_x != x

    if effective_x in curve:
        return curve[int(effective_x)], effective_x, was_clamped

    for left, right in zip(coordinates, coordinates[1:]):
        if left <= effective_x <= right:
            value = linear_interpolate(
                effective_x,
                float(left),
                curve[left],
                float(right),
                curve[right],
            )
            return value, effective_x, was_clamped

    raise RuntimeError("Unable to bracket the interpolation coordinate")
