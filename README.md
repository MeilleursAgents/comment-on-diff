This github action can add a comment on a pull request depending on which files are modified.

To use it you need a github workflow like this:
```
name: Notices
on: [pull_request]
jobs:
  build:
    name: Send notices
    runs-on: ubuntu-latest
    steps:
      - name: Check out code
        uses: actions/checkout@v2
      - name: Fetch branches
        run: |
          git fetch --no-tags --prune --depth=100 origin "+refs/heads/${BASE}:refs/remotes/origin/${BASE}"
          git fetch --no-tags --prune --depth=100 origin "+refs/heads/${HEAD}:refs/remotes/origin/${HEAD}"
        env:
          BASE: ${{ github.base_ref }}
          HEAD: ${{ github.head_ref }}
      - name: Comment on diff
        uses: erdnaxeli/comment-on-diff@master
        with:
          base: ${{ github.event.pull_request.base.sha }}
          head: ${{ github.event.pull_request.head.sha }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

You also need a config file named `.github/comment-on-diff.yaml`, wich is a YAML dict where keys are paths regexes and value are the message to send.

Example:
```
main.py: You have changed the main.py file, don't forget to run the linter.
some/folder: Any modification on this folder implies you agree with something.
.+/a?b.py: hey looks at that regex!
```

With this a modification on those files will trigger a comment with the corresponding message:
* `main.py`: "You have changed…"
* `some/folder/any/file`: "Any modification…"
* `something/ab.py`: "hey…"
* `somethingelse/very/far/away/b.py`: "hey…"

Beware that the regex is matched from the start of the file path, so `ab?c.py` would match `abc.py` but not `somewhere/abc.py`.

The messages can be on [multiple lines](https://adminswerk.de/multi-line-string-yaml-ansible-I/) and can use markdown.

The action takes care of not sending twice the same message, to not spam the PR.
