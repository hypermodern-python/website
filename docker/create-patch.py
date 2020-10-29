#!/usr/bin/env python
import argparse
import sys
import subprocess
from pathlib import Path


def create_patch(path: Path, append: bool):
    version = int(path.suffix[1:])
    if version < 1:
        sys.exit(f"version must be a positive integer: {path}")

    path = path.resolve()
    patch = Path(f"{path}.patch")
    canonical = path.parent / path.stem
    previous = (
        canonical if version == 1 else (path.parent / f"{path.stem}.{version - 1:02}")
    )

    for project in path.parents:
        if project.name == "hypermodern-python" and project.parent.name == "docker":
            docker = project.parent
            break
    else:
        sys.exit(f"cannot find root: {path}")

    dockerfile = docker / "Dockerfile"
    args = previous.relative_to(project), path.relative_to(project)
    process = subprocess.run(
        ["diff", "-u", *args],
        cwd=project,
        capture_output=True,
        text=True,
    )

    lines = process.stdout.splitlines(keepends=True)
    lines[0:2] = [
        line.replace(str(arg), str(Path(prefix) / canonical.relative_to(project)))
        for arg, line, prefix in zip(args, lines[0:2], "ab")
    ]

    patch.write_text("".join(lines))

    statements = f"""\
COPY {patch.relative_to(docker)} /tmp/patch
RUN patch -p1 < /tmp/patch
"""

    if append:
        with dockerfile.open("a") as io:
            io.write(statements)
    else:
        sys.stdout.write(statements)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--append", action="store_true", help="Append statements to Dockerfile")
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    for arg in args.files:
        create_patch(Path(arg), append=args.append)


if __name__ == "__main__":
    main()
