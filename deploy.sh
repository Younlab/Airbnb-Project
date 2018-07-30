#!/usr/bin/env bash

pipenv lock --requirements > requirements.txt
git add -f .secrets/ requirements.txt
git add -A
eb deploy --profile fc-pr-user --staged
git reset HEAD .secrets/ requirements.txt
rm requirements.txt
