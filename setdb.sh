#!/usr/bin/env bash

HOST=$(myairbnbproject.ccrdezcnkmuh.ap-northeast-2.rds.amazonaws.com)
USER=$(leesoo)
PORT=$(5432)
DB=$(postgres)
PASSWORD=$(michael6295)

DB_NAME=$(airbnb_rds)

psql --host=${HOST} --user=${USER} --port=${PORT} ${DB}
${PASSWORD}

DROP DATABASE ${DB_NAME};
CREATE DATABASE ${DB_NAME} OWNER ${USER};
\q
