## About this sample project

This sample project is created to provide some skeleton app to work on.
Please don't forget to:
- Change IPs in the bitbucket-pipelines.uml


## Install & Run Locally

This project contains docker integration. You can run it with `pipenv run go-docker`.

In any case before you need to write your `.env` file with correct variables: when using the dockerized
local development setup, copy `.env.local`; otherwise copy `.env.example` to `.env`, and modifiy
accordingly.


## Add git hooks

We are using prospectr + pre-commit to make things workable and clear. Before write any code you need to install
dev dependencies and run `pre-commit install -f` after that. Then whenever you run `git commit` you'll have a fancy
output with checks according to our code standards.

## Prepare a new branch for your work

Work on new `bug/features` will be done in a new branch (*)
There is a convention in the name of the branches used:
**`1-short-description-of-purpose`**

Naming a Branch:
    - Start branch name with the Issue Number: `#1 Initial Issue` > `1-initial-branch-name`
    - Use lowercase only
    - Use dashes to separate words

## Make awesome commits

Commits are the smallest portion of code that can be reviewed and has a
purpose in the codebase. Each commit counts in a branch, not only the full set
of changes.

Please follow this guideline:
https://udacity.github.io/git-styleguide/

To use cool github linking to the issue please add #taskNumber in the end. E.g.:

`docs: add changes to the Readme #123`

## Documentation

Please make sure that each public class, method and function has meaningful documentation which describes the purpose of the code.
To make things easier to follow we use Python annotations to the public functions and method.
Cheat sheet:
https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html

More info here:
https://docs.python.org/3/library/typing.html
