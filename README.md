# FEA Structural Automation

[![quality](https://github.com/erickjer0288-droid/fea-structural-automation/actions/workflows/quality.yml/badge.svg)](https://github.com/erickjer0288-droid/fea-structural-automation/actions/workflows/quality.yml)

A sanitized Python engineering toolkit for fast structural and sealing calculations before detailed finite element analysis.

> **Portfolio safety:** this repository excludes proprietary geometry, client names, internal reports, and private source curves. Included curve values are illustrative and must not be used for production release.

## Why this project exists

Detailed nonlinear contact analysis is valuable, but early engineering decisions often need a transparent first-pass model. This project turns a personal O-ring squeeze quick-screen into a typed, tested, installable Python package with traceable assumptions and explicit limitations.

## Current capability

The first workflow evaluates an MMC-driven squeeze target and reports:

- updated LMC, nominal, and MMC squeeze;
- approximate groove-depth adjustment;
- nearest available illustrative cross-section;
- nominal line-load estimate across squeeze and Shore A;
- lbf/in and N/mm results;
- flags when interpolation inputs are clamped or approximated.

## Engineering workflow

```text
Design inputs
    |
    v
Input validation
    |
    v
MMC-driven squeeze update
    |
    v
Cross-section curve selection
    |
    v
Squeeze interpolation + Shore interpolation
    |
    v
Screening result and traceability flags
    |
    v
Decision: refine geometry, obtain approved data, or proceed to FEA
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e .
```

For development tools:

```bash
pip install -e .[dev]
```

## Command-line example

```bash
fea-oring-screen \
  --cross-section-mm 1.78 \
  --shore-a 80 \
  --target-mmc 30
```

## Python API

```python
from fea_structural_automation import OringStudy, evaluate_oring_study

study = OringStudy(
    cross_section_mm=1.78,
    shore_a=80.0,
    target_mmc_percent=30.0,
)
result = evaluate_oring_study(study)

print(result.squeeze)
print(result.nominal_line_load_n_per_mm)
```

## Repository structure

```text
src/fea_structural_automation/
├── cli.py             Command-line interface
├── curves.py          Explicitly illustrative screening curves
├── interpolation.py   Dependency-free interpolation utilities
├── models.py          Typed input and result models
├── squeeze.py         Engineering calculation engine
└── units.py           Unit conversions

tests/                 Unit tests and edge cases
docs/                  Methodology and assumptions
examples/              Minimal executable examples
.github/workflows/      Automated lint, typing, and tests
```

## Quality controls

Every pull request runs:

- Ruff linting;
- strict MyPy checks on the package;
- Pytest with coverage;
- Python 3.10, 3.11, and 3.12 compatibility checks.

Run the same checks locally:

```bash
ruff check .
mypy src
pytest
```

## Engineering limitations

This package is an early-stage screening tool. It does not model nonlinear elastomer material response, frictional contact, thermal effects, aging, compression set, pressure energization, gland fill, stretch, or full tolerance propagation. The nearest illustrative cross-section is selected and squeeze requests outside the curve domain are clamped.

Read the detailed methodology in [`docs/methodology.md`](docs/methodology.md).

## Roadmap

- Approved CSV curve import with metadata and units.
- Sensitivity and tolerance propagation.
- Automated plots and engineering report generation.
- Reproducible notebook case study.
- Comparison against a generic nonlinear contact FEA model.
- Versioned releases and expanded documentation.

## License

MIT License. See [`LICENSE`](LICENSE).

## Resumen en español

Este repositorio transforma un cálculo preliminar de squeeze de O-ring en una herramienta Python profesional, reutilizable y verificable. Todos los datos públicos son ilustrativos; cualquier aplicación real requiere datos aprobados, validación física y revisión de ingeniería.
