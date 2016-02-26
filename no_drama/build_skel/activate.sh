#!/bin/bash
FILES=bootstrap_wheels/*.whl
for f in $FILES
do
  echo "adding $f to PYTHONPATH"
  export PYTHONPATH=${PYTHONPATH}:${f}
done

python -m virtualenv --no-pip --no-wheel --no-setuptools empty_venv
python -m virtualenv --extra-search-dir=bootstrap_wheels venv

SITE_PACKAGES=`find venv -name 'site-packages'`
echo `python lib/dfd.py build_lib`>$SITE_PACKAGES/no_drama.pth
echo `python lib/dfd.py django_root`>>$SITE_PACKAGES/no_drama.pth

venv/bin/pip install wheels/*.whl
venv/bin/django-admin collectstatic --noinput
venv/bin/python -m activate_phase2
