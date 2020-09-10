#!/usr/bin/env python

import json
from os import environ

from git import Repo
from github import Github


CONFIG = {
    "main.py": "MAIN",
    "toto": "you change toto you motherfucker",
}


with open(environ["GITHUB_EVENT_PATH"]) as f:
    event = json.load(f)

github = Github(environ["GITHUB_TOKEN"])
gh_repo = github.get_repo(event["repository"]["full_name"])
gh_pr = gh_repo.get_pull(event["number"])


repo = Repo(".")
for diff in repo.commit(environ["HEAD"]).diff(repo.commit(environ["BASE"])):
    for path in CONFIG:
        if diff.a_path.startswith(path) or diff.b_path.startswith(path):
            gh_pr.create_issue_comment(CONFIG["path"])
