#!/usr/bin/env python

import json
import logging
import re
from os import environ
from typing import List, Tuple, TypedDict, Union

import yaml
from git import Repo
from github import Github


logging.basicConfig(level=logging.INFO)


# We will fetch comments later if needed. This avoids an uneeded API call.
gh_comments: List[str] = []


class Params(TypedDict):
    msg: str
    absent: bool


def check_match(regex: str, tests: List[str]) -> bool:
    """Check if the regex matches the any string in `tests`."""
    return any(re.match(regex, test) for test in tests)


def read_params(params: Union[str, Params]) -> Tuple[str, bool]:
    """Read parameters.

    The source can be either a string or a dict. It applies default values and
    return all parameters as a tuple.
    """
    if isinstance(params, str):
        msg = params
        absent = False
    elif isinstance(params, dict):
        msg = params["msg"]
        absent = params["absent"]

    return msg, absent


def send_comment(msg: str) -> None:
    """Send a comment to github

    If the comment was already sent, do not send it again.
    """
    global gh_comments
    if not gh_comments:
        gh_comments = [c.body for c in gh_pr.get_issue_comments()]

    if msg not in gh_comments:
        gh_pr.create_issue_comment(msg)


if __name__ == "__main__":
    with open(".github/comment-on-diff.yaml") as f:
        CONFIG = yaml.safe_load(f)

    with open(environ["GITHUB_EVENT_PATH"]) as f:
        event = json.load(f)

    github = Github(environ["INPUT_GITHUB_TOKEN"])
    gh_repo = github.get_repo(event["repository"]["full_name"])
    gh_pr = gh_repo.get_pull(event["number"])

    repo = Repo(".")
    head = environ["INPUT_HEAD"]
    base = environ["INPUT_BASE"]
    merge_base = repo.merge_base(head, base)

    absent_diffs_found: List[str] = []

    # We look for all diffs
    for diff in repo.commit(head).diff(merge_base):
        logging.info(f"Checking diff between {diff.a_path} and {diff.b_path}")
        for path, params in CONFIG.items():
            msg, absent = read_params(params)

            if check_match(path, [diff.a_path, diff.b_path]):
                logging.info(f"Found a matching rules: '{path}'")
                if absent:
                    # We register this diff was found, but we don't send a comment
                    absent_diffs_found.append(path)
                    continue

                send_comment(msg)

    # We look for missing diffs
    logging.info("Checking missing diffs")
    for path, params in CONFIG.items():
        msg, absent = read_params(params)
        if not absent:
            continue

        logging.info(f"Checking rule '{path}'")
        # Did we found the diff?
        if path in absent_diffs_found:
            logging.info(f"The diff for rule '{path}' was found, not sending a comment")
            continue

        send_comment(msg)
