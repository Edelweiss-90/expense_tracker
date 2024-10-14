import sqlite3
from typing import Self, Union


class SQL:
    _instance = None

    @classmethod
    def instance(cls, db_name) -> Self:
        if cls._instance:
            return cls._instance

        cls._instance = cls.__new__(cls)
        cls._instance.conn = sqlite3.connect(db_name)
        cls._instance.conn.row_factory = sqlite3.Row
        cls._instance.cur = cls._instance.conn.cursor()

    @classmethod
    def create_table(cls, script: str) -> None:
        cls._instance.cur.execute(script)

    @classmethod
    def insert_data(cls, script) -> int:
        cls._instance.cur.execute(script)
        cls._instance.conn.commit()

        return cls._instance.cur.lastrowid

    @classmethod
    def delete_data(cls, script: str) -> None:
        cls._instance.cur.execute(script)

        cls._instance.conn.commit()

    @classmethod
    def find_one(cls, script: str) -> Union[None, object]:
        res = cls._instance.cur.execute(script)
        entity = res.fetchone()
        if entity:
            return dict(entity)

        return None

    @classmethod
    def find_many(cls, script: str) -> object:
        res = cls._instance.cur.execute(script)
        rows = res.fetchall()
        return [dict(row) for row in rows]
