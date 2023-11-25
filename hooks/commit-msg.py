#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

from colorama import Back, Style


def check_git_commit_name(msg):
    if re.match(r"^(feat|fix|doc|test|perf|refacto|chore):([ \w]+)$", msg):
        return 0
    print(
        f"{Back.RED} Message commit match regex {Style.RESET_ALL}.",
        f"Invalid: {msg}",
        "Valid example: feat: my commit message",
        sep="\n",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    commit_msg = ""
    with open(sys.argv[1], "r") as file_msg:
        commit_msg = file_msg.read()
    result = check_git_commit_name(commit_msg)
    sys.exit(result)
