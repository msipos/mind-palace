#!/bin/bash

set -e

if [[ -z "${MIND_PALACE_SQLITE}" ]]; then
  export MIND_PALACE_SQLITE="/app/data/db.sqlite"
fi

python /app/manage.py $@
