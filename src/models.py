from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


JsonType = Literal[
    "number",
    "string",
    "boolean",
    "integer",
    "array",
    "object",
    "null",
]


class FunctionParameterDefinition(BaseModel):

    model_config = ConfigDict(extra="forbid")

    type: JsonType


class FunctionDefinition(BaseModel):

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    name: str
    description: str
    parameters: dict[str, FunctionParameterDefinition]
    returns_: FunctionParameterDefinition = Field(alias="returns")


class PromptItem(BaseModel):

    model_config = ConfigDict(extra="forbid")

    prompt: str


class FunctionCallResult(BaseModel):

    model_config = ConfigDict(extra="forbid")

    prompt: str
    name: str
    parameters: dict[str, Any]
