from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from src.models import FunctionDefinition, PromptItem


class ParserError(Exception):
    """Raised when project input files are missing or invalid."""


def _load_json_file(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ParserError(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        message = (
            f"Invalid JSON in {path} at line {exc.lineno}, "
            f"col {exc.colno}: {exc.msg}"
        )
        raise ParserError(message) from exc
    except OSError as exc:
        raise ParserError(f"Could not read input file {path}: {exc}") from exc


def load_function_definitions(path: Path) -> list[FunctionDefinition]:
    raw_data = _load_json_file(path)
    if not isinstance(raw_data, list):
        raise ParserError(
            "Functions definition file must contain a JSON array: "
            f"{path}"
        )

    parsed: list[FunctionDefinition] = []
    for index, item in enumerate(raw_data):
        try:
            parsed.append(FunctionDefinition.model_validate(item))
        except ValidationError as exc:
            raise ParserError(
                "Invalid function definition at index "
                f"{index} in {path}: {exc}"
            ) from exc

    if not parsed:
        raise ParserError(f"Functions definition file is empty: {path}")
    return parsed


def load_prompt_items(path: Path) -> list[PromptItem]:
    raw_data = _load_json_file(path)
    if not isinstance(raw_data, list):
        raise ParserError(
            f"Prompt input file must contain a JSON array: {path}"
        )

    parsed: list[PromptItem] = []
    for index, item in enumerate(raw_data):
        try:
            parsed.append(PromptItem.model_validate(item))
        except ValidationError as exc:
            raise ParserError(
                f"Invalid prompt at index {index} in {path}: {exc}"
            ) from exc

    return parsed


def load_inputs(
    functions_definition_path: Path,
    prompts_path: Path,
) -> tuple[list[FunctionDefinition], list[PromptItem]]:
    function_definitions = load_function_definitions(functions_definition_path)
    prompts = load_prompt_items(prompts_path)
    return function_definitions, prompts
