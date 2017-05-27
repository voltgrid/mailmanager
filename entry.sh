#!/usr/bin/env bash

set -ex

# App Defaults
export WORKERS=${WORKERS:-4}
export LOGFILE=${LOGFILE:-/srv/log/web.log}
export PORT=${PORT:-8000}

# alias docker links variables

# SMTP SERVICE
export EMAIL_HOST=${EMAIL_HOST:-${SMTP_PORT_25_TCP_ADDR:-localhost}}
export EMAIL_PORT=${EMAIL_PORT:-${SMTP_PORT_25_TCP_PORT:-25}}

# MYSQL SERVICE
export DATABASE_NAME=${DATABASE_NAME:-mail}
export DATABASE_USER=${DATABASE_USER:-root}
export DATABASE_PASS=${DATABASE_PASS}
export DATABASE_HOST=${DATABASE_HOST:-$MARIADB_PORT_3306_TCP_ADDR}
export DATABASE_PORT=${DATABASE_PORT:-$MARIADB_PORT_3306_TCP_PORT}

echo "Exec'ing $@"
exec "$@"
