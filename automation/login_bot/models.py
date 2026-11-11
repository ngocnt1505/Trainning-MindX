from dataclasses import dataclass, field
from enum import Enum


AUTO_TAG = "auto-processed"


@dataclass(frozen=True)
class Ticket:
    id: int
    subject: str
    description: str = ""
    email: str = ""
    customer: str = ""
    tags: tuple = ()


@dataclass(frozen=True)
class Employee:
    email: str
    name: str
    status: str  # "active" | "terminated"
    department: str = ""


@dataclass(frozen=True)
class LmsAccount:
    email: str
    status: str  # "active" | "deactivated"
    last_login: str = ""


class Outcome(str, Enum):
    NOT_LOGIN = "not_login"
    REACTIVATED = "reactivated"
    PASSWORD_RESET = "password_reset"
    TERMINATED = "terminated"
    ESCALATED = "escalated"
    FAILED = "failed"
    ALREADY_PROCESSED = "already_processed"


# Kết quả bot tự giải quyết được, không cần người xử lý.
AUTOMATED_OUTCOMES = {Outcome.REACTIVATED, Outcome.PASSWORD_RESET}


@dataclass
class Result:
    ticket_id: int
    outcome: Outcome
    reason: str = ""
    actions: list = field(default_factory=list)
