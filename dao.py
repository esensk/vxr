# -*- coding:utf-8 -*-

import mysql.connector
import settings

conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='docker',
    password=settings.DB_PASSWORD,
    database='vxr',
)

conn.ping(reconnect=True)

print(conn.is_connected())
