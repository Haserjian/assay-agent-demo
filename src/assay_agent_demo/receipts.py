"""Canonical serialization helpers and receipt objects for the demo."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any


class DemoEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class ReceiptType(DemoEnum):
    CUSTOMER_REPORT = "customer_report_receipt"
    LOG_EXCERPT = "log_excerpt_receipt"
    MISSING_REPRO = "missing_repro_receipt"
    DUPLICATE_ISSUE = "duplicate_issue_receipt"
    POLICY_RULE = "policy_rule_receipt"
    APPROVAL = "approval_receipt"
    SEVERITY_EVIDENCE = "severity_evidence_receipt"


@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    receipt_type: ReceiptType | str
    claim: str
    body: str | Mapping[str, Any]
    source: str

    def __post_init__(self) -> None:
        if not self.receipt_id:
            raise ValueError("receipt_id must be non-empty")
        if not self.claim:
            raise ValueError("claim must be non-empty")
        object.__setattr__(self, "receipt_type", ReceiptType(self.receipt_type))
        object.__setattr__(self, "body", freeze_data(self.body))

    def to_json(self) -> dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "receipt_type": self.receipt_type,
            "claim": self.claim,
            "body": self.body,
            "source": self.source,
        }


def freeze_data(value: Any) -> Any:
    if isinstance(value, Enum):
        return value
    if is_dataclass(value):
        return value
    if isinstance(value, Mapping):
        return MappingProxyType(
            {str(key): freeze_data(item) for key, item in value.items()}
        )
    if isinstance(value, (tuple, list)):
        return tuple(freeze_data(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return tuple(sorted(freeze_data(item) for item in value))
    return value


def to_canonical_data(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    to_json = getattr(value, "to_json", None)
    if callable(to_json):
        return to_canonical_data(to_json())
    if is_dataclass(value):
        return {
            item.name: to_canonical_data(getattr(value, item.name))
            for item in fields(value)
        }
    if isinstance(value, Mapping):
        return {
            str(key): to_canonical_data(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [to_canonical_data(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted(to_canonical_data(item) for item in value)
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    raise TypeError(f"cannot canonicalize {type(value).__name__}")


def to_canonical_json(value: Any) -> str:
    return json.dumps(
        to_canonical_data(value),
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def stable_hash(value: Any) -> str:
    return hashlib.sha256(to_canonical_json(value).encode("utf-8")).hexdigest()


__all__ = [
    "DemoEnum",
    "Receipt",
    "ReceiptType",
    "freeze_data",
    "stable_hash",
    "to_canonical_data",
    "to_canonical_json",
]
