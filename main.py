#!/usr/bin/env python

import json
from os import environ
from typing import List

from git import Repo
from github import Github


CONFIG = {
    "main.py": "MAIN",
    "toto": "you change toto you motherfucker",
}


with open(environ["GITHUB_EVENT_PATH"]) as f:
    event = json.load(f)

github = Github(environ["INPUT_GITHUB_TOKEN"])
gh_repo = github.get_repo(event["repository"]["full_name"])
gh_pr = gh_repo.get_pull(event["number"])
# We will fetch comments later if needed. This avoids an uneeded API call.
gh_comments: List[str] = []


repo = Repo(".")
for diff in repo.commit(environ["INPUT_HEAD"]).diff(repo.commit(environ["INPUT_BASE"])):
    for path, msg in CONFIG.items():
        if diff.a_path.startswith(path) or diff.b_path.startswith(path):
            if not gh_comments:
                gh_comments = [c.body for c in gh_pr.get_issue_comments()]

            if msg not in gh_comments:
                gh_pr.create_issue_comment(CONFIG[msg])
