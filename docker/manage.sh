#!/bin/bash

set -e

if [[ -z "${MIND_PALACE_SQLITE}" ]]; then
  export MIND_PALACE_SQLITE="/app/data/db.sqlite"
fi

if [[ -z "${MIND_PALACE_CACHE}" ]]; then
  export MIND_PALACE_CACHE="/app/cache"
fi

if [[ -z "${MIND_PALACE_EXPORTS}" ]]; then
  export MIND_PALACE_EXPORTS="/app/exports"
fi

python /app/manage.py $@
