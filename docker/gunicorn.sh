#!/bin/bash

if [[ -z "${MIND_PALACE_SQLITE}" ]]; then
  export MIND_PALACE_SQLITE="/app/data/db.sqlite"
fi

if [[ -z "${MIND_PALACE_CACHE}" ]]; then
  export MIND_PALACE_CACHE="/app/cache"
fi

if [[ -z "${MIND_PALACE_EXPORTS}" ]]; then
  export MIND_PALACE_EXPORTS="/app/exports"
fi

if [[ -z "${MIND_PALACE_NO_MIGRATE}" ]]; then
  python /app/manage.py migrate
fi

if [[ -z "${MIND_PALACE_NO_CREATE_ADMIN}" ]]; then
  python /app/manage.py create_admin
fi

if [[ -z "${MIND_PALACE_GUNICORN_WORKERS}" ]]; then
  MIND_PALACE_GUNICORN_WORKERS=2
fi

gunicorn mind_palace.mind_palace_site.wsgi -w $MIND_PALACE_GUNICORN_WORKERS --log-level debug -b 0.0.0.0:8000
