from enum import Enum
from pydantic import BaseModel


class TaskType(str, Enum):
    summarize = "summarize"
    expand = "expand"
    polish = "polish"
    action_items = "action_items"


class TaskResult(BaseModel):
    task: TaskType
    result: str


class ProcessResponse(BaseModel):
    transcription: str
    results: list[TaskResult]
    metadata: dict


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail
