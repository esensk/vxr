# -*- coding:utf-8 -*-

import mysql.connector
from urllib.parse import urlparse


class Dao:
    def __init__(self, url_str):
        url = urlparse(url_str)

        host = url.hostname
        port = url.port
        user = url.username
        password = url.password
        database = url.path[1:]

        assert host and port and user and password and database

        self.__conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
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
            public_id = "{public_id}"
            and password = "{password}"
        """.format(public_id=public_id, password=password)
        )

        rows = cur.fetchall()
        cur.close()
        return rows

    def __can_insert_user(self, public_id, password):
        return len(self.select_user(public_id, password)) == 0

    def insert_user(self, public_id, password):
        if not self.__can_insert_user(public_id, password):
            return False

        cur = self.__conn.cursor()

        try:
            cur.execute("""
            insert into
                t_user (public_id, password)
            values("{public_id}", "{password}")
            """.format(public_id=public_id, password=password))
            self.__conn.commit()
            cur.close()
            return True
        except Exception as e:
            self.__conn.rollback()
            raise e

    def __can_update_user(self, public_id, password):
        return len(self.select_user(public_id, password)) > 0

    def update_user(self, public_id, password, new_public_id, new_password):
        assert not ((new_public_id is None or new_public_id == "") and
                    (new_password is None or new_password == ""))

        if not self.__can_update_user(public_id, password):
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
                public_id = "{new_public_id}",
                password = "{new_password}"
            where
                public_id = "{public_id}"
                and password = "{password}"
            """.format(new_public_id=new_public_id, new_password=new_password,
                       public_id=public_id, password=password))
            self.__conn.commit()
            cur.close()
            return True
        except Exception as e:
            self.__conn.rollback()
            raise e

    def __can_delete_user(self, public_id, password):
        return len(self.select_user(public_id, password)) > 0

    def delete_user(self, public_id, password):
        if not self.__can_delete_user(public_id, password):
            return False

        cur = self.__conn.cursor()

        try:
            cur.execute("""
            delete from
                t_user
            where
                public_id = "{public_id}"
                and password = "{password}"
            """.format(public_id=public_id, password=password))
            self.__conn.commit()
            cur.close()
            return True
        except Exception as e:
            self.__conn.rollback()
            raise e

    def select_effector_by_id(self, id):
        cur = self.__conn.cursor()

        cur.execute("""
        select
            *
        from
            t_effector
        where
            id = "{id}"
        """.format(id=id)
        )

        rows = cur.fetchall()
        cur.close()
        return rows

    def select_effector_by_creator_id(self, creator_id):
        cur = self.__conn.cursor()

        cur.execute("""
        select
            *
        from
            t_effector
        where
            creator_id = "{creator_id}"
        """.format(creator_id=creator_id)
        )

        rows = cur.fetchall()
        cur.close()
        return rows

    def insert_effector(self, creator_id, code):
        assert code

        cur = self.__conn.cursor()

        try:
            cur.execute("""
            insert into
                t_effector (creator_id, code)
            values("{creator_id}", "{code}")
            """.format(creator_id=creator_id, code=code))
            self.__conn.commit()
            cur.close()
            return True
        except Exception as e:
            self.__conn.rollback()
            raise e

    def __can_update_effector(self, id):
        return len(self.select_effector_by_id(id)) > 0

    def update_effector(self, id, new_code):
        if not self.__can_update_effector(id):
            return False

        assert new_code

        cur = self.__conn.cursor()

        try:
            cur.execute("""
            update
                t_effector
            set
                code = "{new_code}"
            where
                id = "{id}"
            """.format(id=id))
            self.__conn.commit()
            cur.close()
            return True
        except Exception as e:
            self.__conn.rollback()
            raise e

    def __can_delete_effector(self, id):
        return len(self.select_effector_by_id(id)) > 0

    def delete_effector(self, id):
        if not self.__can_delete_effector(id):
            return False

        cur = self.__conn.cursor()

        try:
            cur.execute("""
            delete from
                t_effector
            where
                id = "{id}"
            """.format(id=id))
            self.__conn.commit()
            cur.close()
            return True
        except Exception as e:
            self.__conn.rollback()
            raise e
