# Methodology

## Purpose

This package supports preliminary engineering screening for an O-ring squeeze stack. It estimates how an MMC-driven squeeze target changes the LMC and nominal squeeze values, then evaluates an illustrative nominal line load.

## Calculation sequence

1. Validate the cross-section, Shore A hardness, MMC target, and geometric calibration.
2. Compare the requested MMC target with the baseline MMC squeeze.
3. Apply the same percentage-point reduction to LMC and nominal squeeze.
4. Convert the reduction into an approximate groove-depth adjustment.
5. Select the nearest available illustrative cross-section curve.
6. Interpolate line load across squeeze percentage.
7. Interpolate or extrapolate across Shore A hardness.
8. Report both lbf/in and N/mm, plus approximation and clamp flags.

## Baseline example

The default baseline is deliberately exposed as an input model rather than hidden in the algorithm:

- LMC: 18%
- Nominal: 25%
- MMC: 33%
- Geometric calibration: 0.021 mm per percentage point

These values are a generic demonstration baseline. They are not universal O-ring design recommendations.

## Data policy

The repository does not include the original private source curves. The included values are illustrative and intentionally separated in `curves.py`. A future release will support importing approved CSV data with source metadata.

## Limitations

This quick-screen does not represent nonlinear elastomer behavior, contact friction, thermal effects, aging, compression set, gland fill, stretch, pressure energization, manufacturing variation beyond the simplified squeeze stack, or validation against physical testing.

Use the output to organize early design questions, not to approve production hardware.
