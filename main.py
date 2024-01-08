#!/usr/bin/env python

import json
import logging
import re
from os import environ
from typing import TypedDict

import yaml
from git import GitConfigParser, Repo
from git.config import get_config_path
from github import Github


logging.basicConfig(level=logging.INFO)


# We will fetch comments later if needed. This avoids an uneeded API call.
gh_comments: list[str] = []


class Params(TypedDict):
    msg: str
    absent: bool


def check_match(regex: str, tests: list[str]) -> bool:
    """Check if the regex matches the any string in `tests`."""
    return any(re.match(regex, test) for test in tests)


def read_params(params: str | Params) -> tuple[str, bool]:
    """
    Read parameters.

    The source can be either a string or a dict. It applies default values and
    return all parameters as a tuple.
    """
    if isinstance(params, str):
        msg = params
        absent = False
    elif isinstance(params, dict):
        msg = params["msg"]
        absent = params["absent"]
    else:
        raise ValueError(f"Unknown parameters '{params}'")

    return msg, absent


def normalize_comment(comment: str) -> str:
    """
    Normalize a comment.

    It does the following:
      * uncheck checked boxes
    """
    fixed = comment.replace("[x]", "[ ]")
    return fixed


def send_comment(msg: str) -> None:
    """
    Send a comment to Github.

    If the comment was already sent, do not send it again.
    """
    global gh_comments
    if not gh_comments:
        gh_comments = [normalize_comment(c.body) for c in gh_pr.get_issue_comments()]

    if normalize_comment(msg) not in gh_comments:
        gh_pr.create_issue_comment(msg)
        gh_comments.append(msg)


if __name__ == "__main__":
    with open(".github/comment-on-diff.yaml") as f:
        CONFIG = yaml.safe_load(f)

    with open(environ["GITHUB_EVENT_PATH"]) as f:
        event = json.load(f)

    github = Github(environ["INPUT_GITHUB_TOKEN"])
    gh_repo = github.get_repo(event["repository"]["full_name"])
    gh_pr = gh_repo.get_pull(event["number"])

    workspace = environ["GITHUB_WORKSPACE"]
    GitConfigParser(
        get_config_path("global"), read_only=False, config_level="global"
    ).add_value("safe", "directory", workspace).release()

    repo = Repo(workspace)
    head = environ["INPUT_HEAD"]
    base = environ["INPUT_BASE"]
    merge_base = repo.merge_base(head, base)

    absent_diffs_found: list[str] = []

    # We look for all diffs
    for diff in repo.commit(head).diff(merge_base):
        logging.info("Checking diff between %s and %s", diff.a_path, diff.b_path)
        for path, params in CONFIG.items():
            msg, absent = read_params(params)

            if check_match(path, [diff.a_path, diff.b_path]):
                logging.info("Found a matching rules: '%s'", path)
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

        logging.info("Checking rule '%s'", path)
        # Did we find the diff?
        if path in absent_diffs_found:
            logging.info(
                "The diff for rule '%s' was found, not sending a comment", path
            )
            continue

        send_comment(msg)
