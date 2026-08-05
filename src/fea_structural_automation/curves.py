"""Illustrative screening curves.

The values in this module are deliberately generic portfolio data. Replace them
with an approved, traceable source before using the package for design work.
"""

from typing import Final

Curve = dict[int, float]
CurveKey = tuple[float, int]

AVAILABLE_CROSS_SECTIONS_IN: Final[tuple[float, ...]] = (
    0.070,
    0.103,
    0.139,
    0.210,
    0.275,
)

ILLUSTRATIVE_LINE_LOAD_CURVES: Final[dict[CurveKey, Curve]] = {
    (0.070, 70): {5: 2.0, 10: 4.5, 20: 12.0, 30: 28.0},
    (0.070, 90): {5: 4.0, 10: 9.0, 20: 24.0, 30: 55.0},
    (0.103, 70): {5: 2.5, 10: 6.0, 20: 18.0, 30: 42.0},
    (0.103, 90): {5: 6.0, 10: 14.0, 20: 38.0, 30: 82.0},
    (0.139, 70): {5: 4.0, 10: 9.0, 20: 26.0, 30: 70.0},
    (0.139, 90): {5: 10.0, 10: 24.0, 20: 78.0, 30: 210.0},
    (0.210, 70): {5: 7.0, 10: 15.0, 20: 38.0, 30: 90.0},
    (0.210, 90): {5: 13.0, 10: 28.0, 20: 70.0, 30: 165.0},
    (0.275, 70): {5: 9.0, 10: 21.0, 20: 50.0, 30: 120.0},
    (0.275, 90): {5: 17.0, 10: 38.0, 20: 92.0, 30: 205.0},
}
