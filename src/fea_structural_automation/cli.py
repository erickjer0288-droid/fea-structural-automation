"""Command-line interface for the O-ring quick-screen example."""

import argparse

from .models import OringStudy
from .squeeze import evaluate_oring_study


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fea-oring-screen",
        description="Run a sanitized O-ring squeeze and line-load quick-screen.",
    )
    parser.add_argument("--cross-section-mm", type=float, required=True)
    parser.add_argument("--shore-a", type=float, required=True)
    parser.add_argument("--target-mmc", type=float, required=True)
    parser.add_argument("--mm-per-percent", type=float, default=0.021)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = evaluate_oring_study(
        OringStudy(
            cross_section_mm=args.cross_section_mm,
            shore_a=args.shore_a,
            target_mmc_percent=args.target_mmc,
            mm_per_percent=args.mm_per_percent,
        )
    )

    print("O-ring engineering quick-screen")
    print(f"Groove-depth adjustment: {result.groove_depth_adjustment_mm:.3f} mm")
    print(
        "Squeeze: "
        f"LMC={result.squeeze.lmc_percent:.2f}%, "
        f"NOM={result.squeeze.nominal_percent:.2f}%, "
        f"MMC={result.squeeze.mmc_percent:.2f}%"
    )
    print(
        "Estimated nominal line load: "
        f"{result.nominal_line_load_lbf_per_in:.2f} lbf/in "
        f"({result.nominal_line_load_n_per_mm:.4f} N/mm)"
    )
    if result.force_lookup_was_clamped:
        print(f"Warning: force lookup clamped to {result.force_lookup_percent:.1f}% squeeze")
    if result.cross_section_was_approximated:
        print(
            "Note: nearest illustrative cross-section used: "
            f"{result.selected_cross_section_in:.3f} in"
        )


if __name__ == "__main__":
    main()
