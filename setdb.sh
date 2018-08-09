#!/usr/bin/env bash

set -o nounset
set -e

echo "START ./setdb.sh"

HOST="myairbnbproject.ccrdezcnkmuh.ap-northeast-2.rds.amazonaws.com"
USER="leesoo"
PORT="5432"
DB="postgres"

export PGPASSWORD="michael6295"
psql --host=${HOST} --user=${USER} --port=${PORT} ${DB}

# psql 접근까지 가능 : 추가 수정 예정
#DB_NAME="airbnb_rds"
#
#echo "DROP DATABASE ${DB_NAME};"
#echo "CREATE DATABASE ${DB_NAME} OWNER ${USER};"
#echo "\q"
