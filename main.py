#!/usr/bin/env python

import json
import re
from os import environ
from typing import List

import yaml
from git import Repo
from github import Github


def check_match(regex: str, path: str) -> bool:
    """Check if the regex matches the given path."""
    return re.match(regex, path) is not None


if __name__ == "__main__":
    with open(".github/comment-on-diff.yaml") as f:
        CONFIG = yaml.safe_load(f)

    with open(environ["GITHUB_EVENT_PATH"]) as f:
        event = json.load(f)

    github = Github(environ["INPUT_GITHUB_TOKEN"])
    gh_repo = github.get_repo(event["repository"]["full_name"])
    gh_pr = gh_repo.get_pull(event["number"])
    # We will fetch comments later if needed. This avoids an uneeded API call.
    gh_comments: List[str] = []

    repo = Repo(".")
    for diff in repo.commit(environ["INPUT_HEAD"]).diff(
        repo.commit(environ["INPUT_BASE"])
    ):
        for path, msg in CONFIG.items():
            if check_match(path, diff.a_path):
                if not gh_comments:
                    gh_comments = [c.body for c in gh_pr.get_issue_comments()]

                if msg not in gh_comments:
                    gh_pr.create_issue_comment(msg)
