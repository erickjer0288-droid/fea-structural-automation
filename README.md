# FEA Structural Automation

Python tools and reproducible workflows for engineering quick-screen calculations used before detailed finite element analysis.

## Project status

This repository is an initial, sanitized portfolio version. It contains a generic O-ring squeeze and reaction-force screening example derived from a personal engineering workflow. Proprietary geometry, client information, internal reports, and source documents are intentionally excluded.

## Current example

The first module estimates:

- updated LMC, nominal, and MMC squeeze values after a target change;
- an approximate groove-depth adjustment;
- nominal line load using illustrative Shore A and cross-section curves;
- unit conversion between lbf/in and N/mm.

The calculation is intended for preliminary screening and education. It is not a substitute for supplier data, validation testing, detailed contact analysis, or a production design release.

## Repository structure

```text
src/fea_structural_automation/   Reusable Python package
examples/                        Command-line example
tests/                           Unit tests
docs/                            Methodology and assumptions
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
python examples/oring_quickscreen.py --cross-section-mm 1.78 --shore-a 80 --target-mmc 30
```

## Example output

```text
Groove-depth adjustment: 0.063 mm
New squeeze values: LMC=15.00%, NOM=22.00%, MMC=30.00%
Estimated nominal line load: 15.43 lbf/in (2.7020 N/mm)
```

## Engineering limitations

- Embedded force values are illustrative and must be replaced with approved supplier or test data for real design work.
- Linear interpolation is used between available points.
- Values outside the supported squeeze range are clamped for screening.
- The nearest available cross-section is selected.
- Results do not include friction, temperature, aging, tolerances beyond the simplified stack, material relaxation, or nonlinear contact behavior.

## Roadmap

- Add CSV-based material-curve import.
- Add uncertainty and tolerance propagation.
- Add plots for squeeze and force curves.
- Add a notebook comparing screening results against a simplified FEA model.
- Add continuous integration and expanded tests.

## License

MIT License. See `LICENSE`.

## Aviso en español

Este repositorio es una versión genérica y saneada para portafolio. Los datos incluidos son ilustrativos y no deben utilizarse para liberar un diseño de producción sin validación independiente.
