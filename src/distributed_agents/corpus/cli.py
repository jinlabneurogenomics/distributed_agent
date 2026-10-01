"""CLI for discovering and validating corpus releases."""

from __future__ import annotations

import argparse
import json
import sys

from .doctor import doctor_release
from .models import CorpusRegistryError
from .registry import available_releases, get_release


PATH_RESOURCES = ("root", "manifest", "skills", "biokg")


def _add_release_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--release",
        default=None,
        help="Release ID override (otherwise environment, then committed default).",
    )


def add_subcommands(parser: argparse.ArgumentParser) -> None:
    """Attach corpus actions to an existing parser."""

    sub = parser.add_subparsers(dest="corpus_command", required=True)

    list_parser = sub.add_parser("list", help="List installed corpus releases.")
    list_parser.add_argument("--json", action="store_true")
    list_parser.set_defaults(corpus_func=_run_list)

    describe = sub.add_parser("describe", help="Describe the selected release.")
    _add_release_argument(describe)
    describe.add_argument("--json", action="store_true")
    describe.set_defaults(corpus_func=_run_describe)

    path = sub.add_parser("path", help="Print a selected-release resource path.")
    _add_release_argument(path)
    path.add_argument(
        "resource",
        help="root, manifest, skills, biokg, or any artifact name in release.json",
    )
    path.set_defaults(corpus_func=_run_path)

    entrypoint = sub.add_parser(
        "entrypoint",
        help="Print a selected-release skill entrypoint by stable role and name.",
    )
    _add_release_argument(entrypoint)
    entrypoint.add_argument("role", help="Stable release skill role, such as ledger.")
    entrypoint.add_argument("name", help="Entrypoint name declared for that role.")
    entrypoint.set_defaults(corpus_func=_run_entrypoint)

    doctor = sub.add_parser("doctor", help="Verify release hashes and integrity.")
    _add_release_argument(doctor)
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(corpus_func=_run_doctor)


def build_parser(*, prog: str = "distributed_agents corpus") -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=prog, description=__doc__)
    add_subcommands(parser)
    return parser


def _run_list(args: argparse.Namespace) -> int:
    releases = available_releases()
    selected = get_release().release_id
    rows = [
        {
            "release_id": release_id,
            "selected": release_id == selected,
            "title": release.manifest["title"],
            "root": str(release.root),
        }
        for release_id, release in sorted(releases.items())
    ]
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        for row in rows:
            marker = "*" if row["selected"] else " "
            print(f"{marker} {row['release_id']}\t{row['title']}\t{row['root']}")
    return 0


def _run_describe(args: argparse.Namespace) -> int:
    release = get_release(args.release)
    if args.json:
        print(json.dumps(release.as_dict(), indent=2))
    else:
        print(f"release_id: {release.release_id}")
        print(f"title: {release.manifest['title']}")
        print(f"root: {release.root}")
        print("artifacts:")
        for name, spec in release.manifest["artifacts"].items():
            print(f"  {name}: {spec['records']} records, {release.resolve(spec['path'])}")
        print("skills:")
        for name in release.manifest["capabilities"]["skills"]["names"]:
            print(f"  {name}")
        print("projections:")
        for name in release.manifest["capabilities"].get("projections", {}):
            print(f"  {name}: {release.projection(name)}")
    return 0


def _run_path(args: argparse.Namespace) -> int:
    release = get_release(args.release)
    if args.resource == "root":
        path = release.root
    elif args.resource == "manifest":
        path = release.manifest_path
    elif args.resource == "skills":
        path = release.skills_root
    elif args.resource == "biokg":
        path = release.projection("biokg")
    else:
        path = release.artifact(args.resource)
    print(path)
    return 0


def _run_entrypoint(args: argparse.Namespace) -> int:
    print(get_release(args.release).skill_entrypoint(args.role, args.name))
    return 0


def _run_doctor(args: argparse.Namespace) -> int:
    result = doctor_release(get_release(args.release))
    if args.json:
        print(json.dumps(result.as_dict(), indent=2))
    else:
        status = "ok" if result.ok else "failed"
        print(f"{result.release_id}: {status} ({len(result.checks)} checks)")
        for warning in result.warnings:
            print(f"warning: {warning}")
        for error in result.errors:
            print(f"error: {error}")
    return 0 if result.ok else 1


def run_from_namespace(args: argparse.Namespace) -> int:
    return args.corpus_func(args)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser(prog="distributed_agents corpus")
    try:
        return run_from_namespace(parser.parse_args(argv))
    except CorpusRegistryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
