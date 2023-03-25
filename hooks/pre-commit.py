#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
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
        # "--check",  # Option to avoid write
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


if __name__ == "__main__":
    path_project = Path(os.getcwd())
    path_venv = path_project.parent
    interpreter = os.path.join(path_venv, "bin", "python3")

    to_run: list = [
        ("Isort", isort_commands),
        ("Black", black_commands),
        ("Flake8", flake_commands),
        ("Bandit", bandit_commands),
        ("Unittest", unittest_commands, "vtasks"),
    ]

    exit_score: int = 0
    print(f"{Back.WHITE+Fore.BLACK} Start pre-commit checks {Style.RESET_ALL}")

    # Checks code quality
    for app in to_run:
        exit_score += run_app(interpreter, path_project, *app)

    if exit_score > 0:
        print(f"\n\n{Back.RED} {exit_score} checks FAILS {Style.RESET_ALL}")
    else:
        print(f"\n\n{Back.GREEN+Fore.BLACK} Checks SUCCESS {Style.RESET_ALL}")

    print("Treatment result", exit_score)
    sys.exit(exit_score)
