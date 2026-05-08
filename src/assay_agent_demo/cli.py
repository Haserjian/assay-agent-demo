"""Command line interface for the deterministic Assay agent demo."""

from __future__ import annotations

import argparse

from .render import render_human, render_json
from .scenarios import list_scenarios, run_scenario


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="assay-agent-demo",
        description="Deterministic support-agent workflow with policy-owned replay.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("list-scenarios", help="list available scenarios")

    run = subcommands.add_parser("run", help="run a scenario")
    run.add_argument("--scenario", required=True, choices=list_scenarios())
    run.add_argument("--format", choices=("human", "json"), default="human")

    replay = subcommands.add_parser("replay", help="replay a scenario")
    replay.add_argument("--scenario", required=True, choices=list_scenarios())
    replay.add_argument("--format", choices=("human", "json"), default="json")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list-scenarios":
        for scenario_id in list_scenarios():
            print(scenario_id)
        return 0

    if args.command in {"run", "replay"}:
        result = run_scenario(args.scenario)
        if args.format == "json":
            print(render_json(result))
        else:
            print(render_human(result))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
