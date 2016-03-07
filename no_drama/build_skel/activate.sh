#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FILES=bootstrap_wheels/*.whl
for f in $FILES
do
  echo "adding $f to PYTHONPATH"
  export PYTHONPATH=${PYTHONPATH}:${f}
done

python -m virtualenv --no-pip --no-wheel --no-setuptools $DIR/empty_venv
python -m virtualenv --extra-search-dir=bootstrap_wheels $DIR/venv

SITE_PACKAGES=`find venv -name 'site-packages'`
echo `python lib/dfd.py build_lib`>$SITE_PACKAGES/no_drama.pth
echo `python lib/dfd.py django_root`>>$SITE_PACKAGES/no_drama.pth

$DIR/venv/bin/wheel install wheels/*.whl --force
$DIR/venv/bin/django-admin.py collectstatic --noinput
$DIR/venv/bin/python -m activate_phase2
