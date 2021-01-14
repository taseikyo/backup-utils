#!/bin/bash
# @Date    : 2020-10-28 18:22:17
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo

[ $# -lt 1  ] &&  echo "$0 <python script>" && exit 1

black $1
isort $1
flake8 --ignore=E203,W503 --max-complexity=25 --max-line-length=88 --statistics --count $1
mypy --ignore-missing-imports $1
pytest --doctest-modules $1
