#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
from pathlib import Path
from subprocess import CompletedProcess, run  # nosec
from typing import Callable

from colorama import Back, Fore, Style


def run_app(
    interpreter: str, path_project: Path, app_name: str, app_method: Callable, *args
) -> int:
    print(f"\n{Back.BLUE+Fore.WHITE}Run {app_name}...{Style.RESET_ALL}")
    commands: list = app_method(interpreter, path_project, *args)
    process: CompletedProcess = run(commands)
    if process.returncode > 0:
        print(f"{Back.RED} {app_name} FAILED {Style.RESET_ALL}")
    else:
        print(f"{Back.GREEN+Fore.BLACK} {app_name} PASSED {Style.RESET_ALL}")
    return process.returncode


def isort_commands(interpreter: str, folder: Path) -> list:
    return [
        interpreter,
        "-m",
        "isort",
        # "--check",  # Option to avoid write
        folder,
    ]


def black_commands(interpreter: str, folder: Path) -> list:
    return [
        interpreter,
        "-m",
        "black",
        "--check",  # Option to avoid write
        folder,
    ]


def flake_commands(interpreter: str, folder: Path) -> list:
    return [
        interpreter,
        "-m",
        "flake8",
        folder,
    ]


def bandit_commands(interpreter: str, folder: Path) -> list:
    return [
        interpreter,
        "-m",
        "bandit",
        "-r",
        folder,
    ]


def unittest_commands(interpreter: str, folder: Path, app_name: str) -> list:
    return [interpreter, "-m", "unittest"]


def coverage_commands(interpreter: str, folder: Path, app_name: str) -> list:
    return [interpreter, "-m", "coverage", "run", "-m", "unittest"]


def check_coverage_report(interpreter: str) -> int:
    process = run(
        [interpreter, "-m", "coverage", "report"],
        capture_output=True,
    )
    print(process.stdout.decode())
    if process.returncode == 0:
        print(f"{Back.GREEN+Fore.BLACK} Coverage report PASSED {Style.RESET_ALL}")
        return 0
    else:
        print(
            f"{Back.RED} Coverage FAIL {Style.RESET_ALL}",
            "Coverage seems too low !",
            sep="\n",
            file=sys.stderr,
        )
        return 1


def check_requirements(interpreter: str) -> int:
    """Check updated requirements"""
    status = 0
    process = run([interpreter, "-m", "pip", "freeze"], capture_output=True)
    content_file_prod = ""
    with open("requirements.txt", "r") as file:
        content_file_prod = file.read()

    content_file_dev = ""
    with open("requirements-dev.txt", "r") as file:
        content_file_dev = file.read()

    content_output = process.stdout.decode().replace("\\n", "\n")

    package_bug = "pkg_resources==0.0.0"
    for req in content_output.split("\n"):
        if (
            req != package_bug
            and req.replace("==", ">=") not in content_file_prod
            and req.replace("==", ">=") not in content_file_dev
        ):
            print(f"missing {req} requirement")
            status += 1

    if status == 0:
        print(f"{Back.GREEN+Fore.BLACK} Requirements PASSED {Style.RESET_ALL}")
        return status
    else:
        print(
            f"{Back.RED} Requirements FAIL {Style.RESET_ALL}"
            "Requirements seems to be outdated",
            sep="\n",
            file=sys.stderr,
        )
        return status


def check_git_branch_name() -> int:
    process = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True)
    branch_name = process.stdout
    if re.match(r"^(bug|feature)-([\w]+)$", branch_name.decode()):
        print(f"{Back.GREEN+Fore.BLACK} Branch name PASSED {Style.RESET_ALL}")
        return 0
    else:
        print(f"{Back.RED} Branch name FAIL {Style.RESET_ALL}", file=sys.stderr)
        print(
            "Please rename your branch with 'bug' or 'feature'"
            " prefix separed by hyphen and followed by some words in snake case",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    path_project = Path(os.getcwd())
    path_venv = path_project.parent
    interpreter = os.path.join(path_venv, "bin", "python3")

    to_run = [
        ("Isort", isort_commands),
        ("Black", black_commands),
        ("Flake8", flake_commands),
        ("Bandit", bandit_commands),
        ("Coverage", coverage_commands, "vtaskr"),
    ]

    exit_score = 0
    print(f"{Back.WHITE+Fore.BLACK} Start pre-commit checks {Style.RESET_ALL}")

    for app in to_run:
        exit_score += run_app(interpreter, path_project, *app)

    exit_score += check_coverage_report(interpreter)
    exit_score += check_requirements(interpreter)
    # exit_score += check_git_branch_name()

    if exit_score > 0:
        print(f"\n\n{Back.RED} {exit_score} checks FAILS {Style.RESET_ALL}")
    else:
        print(f"\n\n{Back.GREEN+Fore.BLACK} Checks SUCCESS {Style.RESET_ALL}")

    print("Treatment result", exit_score)
    sys.exit(exit_score)
