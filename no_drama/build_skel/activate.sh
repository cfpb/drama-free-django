#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FILES=$DIR/bootstrap_wheels/*.whl
for f in $FILES
do
  echo "adding $f to PYTHONPATH"
  export PYTHONPATH=${PYTHONPATH}:${f}
done

python -m virtualenv --no-pip --no-wheel --no-setuptools $DIR/empty_venv
python -m virtualenv --extra-search-dir=$DIR/bootstrap_wheels $DIR/venv

SITE_PACKAGES=`find $DIR/venv -name 'site-packages'`
echo `$DIR/venv/bin/python $DIR/lib/dfd.py build_lib`>$SITE_PACKAGES/no_drama.pth
echo `$DIR/venv/bin/python $DIR/lib/dfd.py django_root`>>$SITE_PACKAGES/no_drama.pth

$DIR/venv/bin/pip install $DIR/wheels/*.whl --force
$DIR/venv/bin/python -m activate_phase2
