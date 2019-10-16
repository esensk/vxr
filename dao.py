# -*- coding:utf-8 -*-

import mysql.connector
import settings


class Dao:
    def __init__(self):
        self.__conn = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='docker',
            password=settings.DB_PASSWORD,
            database='vxr',
        )

        self.__conn.ping(reconnect=True)

    def __del__(self):
        self.__conn.close()

    def is_connected(self):
        return self.__conn.is_connected()

    def select_user(self, public_id, password):
        cur = self.__conn.cursor()

        cur.execute("""
        select
            *
        from
            t_user
        where
            public_id = "${public_id}"
            and password = "${password}"
        """.format(public_id=public_id, password=password)
        )

        rows = cur.fetchall()
        cur.close()
        return rows

    def __can_insert(self, public_id, password):
        return len(self.select_user(public_id, password)) == 0

    def insert_user(self, public_id, password):
        if not self.__can_insert(public_id, password):
            return False

        cur = self.__conn.cursor()

        try:
            cur.execute("""
            insert into
                t_user (public_id, password)
            values("${public_id}", "${password}")
            """.format(public_id=public_id, password=password))
            self.__conn.commit()
            cur.close()
            return True
        except Exception as e:
            self.__conn.rollback()
            raise e

    def __can_update(self, public_id, password):
        return len(self.select_user(public_id, password)) == 0

    def update_user(self, public_id, password, new_public_id, new_password):
        assert not ((new_public_id is None or new_public_id == "") and
                    (new_password is None or new_password == ""))

        if not self.__can_update(public_id, password):
            return False

        if new_public_id is None or new_public_id == "":
            new_public_id = public_id

        if new_password is None or new_password == "":
            new_password = password

        cur = self.__conn.cursor()

        try:
            cur.execute("""
            update
                t_user
            set
                public_id = "${new_public_id}",
                password = "${new_password}"
            where
                public_id = "${public_id}"
                and password = "${password}"
            """.format(new_public_id=new_public_id, new_password=new_password,
                       public_id=public_id, password=password))
            self.__conn.commit()
            cur.close()
            return True
        except Exception as e:
            self.__conn.rollback()
            raise e

    def __can_delete(self, public_id, password):
        return len(self.select_user(public_id, password)) == 0

    def delete_user(self, public_id, password):
        if not self.__can_delete(public_id, password):
            return False

        cur = self.__conn.cursor()

        try:
            cur.execute("""
            delete from
                t_user
            where
                username = "${username}"
                and password = "${password}"
            """.format(public_id=public_id, password=password))
            self.__conn.commit()
            cur.close()
            return True
        except Exception as e:
            self.__conn.rollback()
            raise e
