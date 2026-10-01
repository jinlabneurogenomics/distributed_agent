"""Expose a host HTTP gateway inside a networkless sandbox."""

from __future__ import annotations

import argparse
import socket
import subprocess
import sys
import time
from pathlib import Path


def _wait_ready(port: int, process: subprocess.Popen) -> None:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(
                f"gateway bridge exited before startup ({process.returncode})"
            )
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                return
        except OSError:
            time.sleep(0.05)
    raise TimeoutError(f"gateway bridge did not listen on 127.0.0.1:{port}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--socket", required=True, type=Path)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument(
        "--relay",
        action="append",
        default=[],
        metavar="PORT:SOCKET",
        help="Additional loopback-to-Unix relay (repeatable).",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        parser.error("a command is required after --")

    relay_specs = [(args.port, args.socket)]
    for raw in args.relay:
        port_text, separator, socket_text = raw.partition(":")
        if not separator:
            parser.error(f"invalid --relay {raw!r}; expected PORT:SOCKET")
        relay_specs.append((int(port_text), Path(socket_text)))

    relays = [
        subprocess.Popen(
            [
                "/usr/bin/socat",
                f"TCP4-LISTEN:{port},bind=127.0.0.1,reuseaddr,fork",
                f"UNIX-CONNECT:{socket_path}",
            ],
            stdin=subprocess.DEVNULL,
        )
        for port, socket_path in relay_specs
    ]
    try:
        for (port, _socket_path), relay in zip(relay_specs, relays):
            _wait_ready(port, relay)
        return subprocess.run(command, check=False).returncode
    finally:
        for relay in relays:
            if relay.poll() is None:
                relay.terminate()
        for relay in relays:
            try:
                relay.wait(timeout=5)
            except subprocess.TimeoutExpired:
                relay.kill()
                relay.wait(timeout=5)


if __name__ == "__main__":
    sys.exit(main())
