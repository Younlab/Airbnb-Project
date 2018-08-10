#!/usr/bin/env bash

# 변수선언 실패시 에러 발생시키기, 뭔가 잘 안되면 또 에러 발생시키기!
set -o nounset
set -e

echo "START ./setdb.sh"

HOST='myairbnbproject.ccrdezcnkmuh.ap-northeast-2.rds.amazonaws.com'
USER='leesoo'
PORT='5432'
DB='postgres'
DROP_DB='DROP DATABASE airbnb_rds;'
CREATE_DB='CREATE DATABASE airbnb_rds OWNER leesoo;'

PGPASSWORD='michael6295' psql --host=${HOST} --user=${USER} --port=${PORT} ${DB} -c ${DROP_DB}

PGPASSWORD='michael6295' psql --host=${HOST} --user=${USER} --port=${PORT} ${DB} -c ${CREATE_DB}
