#!/usr/bin/env bash

mysql -u docker -p vxr < "/docker-entrypoint-initdb.d/001-create-table.sql"
