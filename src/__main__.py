from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from src.parser import ParserError, load_inputs


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description="Parse and validate function-calling input files.",
    )
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
        type=Path,
        help="Path to JSON file containing available function definitions.",
    )
    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
        type=Path,
        help="Path to JSON file containing natural language prompts.",
    )
    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json",
        type=Path,
        help="Path where output JSON will be written.",
    )
    return parser


def _write_json(path: Path, payload: list[dict[str, Any]]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    except OSError as exc:
        raise ParserError(f"Failed writing output file {path}: {exc}") from exc


def main() -> int:
    parser = _build_arg_parser()
    args = parser.parse_args()

    try:
        function_definitions, prompts = load_inputs(
            functions_definition_path=args.functions_definition,
            prompts_path=args.input,
        )

        # Placeholder output until constrained decoding is implemented.
        _write_json(args.output, [])

        print(
            "Validated "
            f"{len(function_definitions)} function definitions and "
            f"{len(prompts)} prompts."
        )
        print(
            "Output written to "
            f"{args.output}. "
            "Current output is intentionally empty until decoder is "
            "implemented."
        )
        return 0
    except ParserError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
