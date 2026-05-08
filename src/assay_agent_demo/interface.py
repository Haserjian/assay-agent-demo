"""Interface helpers that propose actions without authorizing them."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .spine import ExecutionSpine


@dataclass(frozen=True)
class InterfaceCommand:
    action_type: str
    attached_receipt_ids: tuple[str, ...] = ()
    params: dict[str, Any] | None = None
    actor: str = "support_agent_interface"

    def __post_init__(self) -> None:
        object.__setattr__(self, "attached_receipt_ids", tuple(self.attached_receipt_ids))


def execute_interface_command(
    spine: ExecutionSpine,
    command: InterfaceCommand,
) -> ExecutionSpine:
    return spine.propose(
        action_type=command.action_type,
        actor=command.actor,
        attached_receipt_ids=command.attached_receipt_ids,
        params=command.params,
    )


__all__ = ["InterfaceCommand", "execute_interface_command"]
