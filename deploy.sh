#!/usr/bin/env bash

pipenv lock --requirements > requirements.txt
git add -f .secrets/ requirements.txt
git add -A
eb deploy --profile airbnb-project-eb --staged
git reset HEAD .secrets/ requirements.txt
rm requirements.txt
