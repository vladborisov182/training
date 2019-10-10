#!/bin/bash
set -x #echo on
cd /srv/project/
eval "$(ssh-agent)"
ssh-add -l
ssh-add ~/.ssh/id_rsa
ssh-add -l
git pull origin release/staging
cd ../
/home/anton/.local/bin/pipenv install
/home/anton/.local/bin/pipenv run ./manage.py migrate
/home/anton/.local/bin/pipenv run ./manage.py collectstatic --noinput
sudo supervisorctl restart myproject
exit