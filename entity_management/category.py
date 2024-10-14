from typing import Union
from db.tables import category
from db.db import SQL
from utils import DeletedStatuses, TableName


class Category:
    __table = category
    __table_name = TableName.CATEGORY.value
    __table_transaction = TableName.TRANSACTION.value

    def __init__(self) -> None:
        SQL.create_table(self.__table)

    def create(self, name: str, parent_id: int) -> Union[None, int]:
        print('TEST 1')
        if not SQL.find_one(f"""SELECT name FROM '{self.__table_name}'
                            WHERE name = '{name}' AND user_id = '{parent_id}'
                            AND
                            deleted_status='{DeletedStatuses.NOT_DELETED.value}'
                            """):
            print('TEST 2')

            return SQL.insert_data(f"""INSERT INTO '{self.__table_name}'
                                   (name, user_id, deleted_status)
                                   VALUES
                                   {
                                       name,
                                       parent_id,
                                       DeletedStatuses.NOT_DELETED.value
                                       }
                                   """)

    def find_one(self, value: tuple, parent_id: int) -> bool:
        category = SQL.find_one(f"""SELECT * FROM '{self.__table_name}'
                                WHERE name = '{value}'
                                AND user_id = '{parent_id}'
                                AND
                                deleted_status =
                                '{DeletedStatuses.NOT_DELETED.value}'
                                """)
        if category:
            return category

        print('Category not found')
        return None

    def get_all(self, parent_id: int) -> list[tuple]:
        return SQL.find_many(f"""SELECT id, name FROM '{self.__table_name}'
                             WHERE user_id= '{parent_id}'
                             AND
                             deleted_status =
                             '{DeletedStatuses.NOT_DELETED.value}'""")

    def category_join_tr(self, category_id: int, user_id: int):
        return SQL.find_many(f"""SELECT
                            c.id as 'id',
                            c.name as 'name',
                            t.id as 'tr_id',
                            t.transaction_date as 'transaction_date',
                            t.amount as 'amount' FROM
                            '{self.__table_name}' c
                            INNER JOIN '{self.__table_transaction}' t
                            ON c.id = t.category_id
                            WHERE c.id = '{category_id}'
                            AND c.user_id = '{user_id}'
                            AND c.deleted_status
                            = '{DeletedStatuses.NOT_DELETED.value}'
                            ORDER BY t.transaction_date ASC
                            """)

    def get_all_ct_with_transaction(self, user_id) -> list[tuple]:
        return SQL.find_many(f"""SELECT
                             c.id as 'id',
                             c.name as 'name',
                             t.id as 'tr_id',
                             t.amount as 'amount',
                             t.transaction_date as 'transaction_date'
                             FROM
                             '{self.__table_name}' c
                             LEFT JOIN
                             '{self.__table_transaction}' t
                             ON c.id = t.category_id
                             WHERE
                             c.user_id = '{user_id}'
                             AND c.deleted_status
                             = '{DeletedStatuses.NOT_DELETED.value}'
                             ORDER BY
                             c.name ASC, t.transaction_date ASC
                             """)

    def delete(self, self_id: int, user_id: int) -> None:
        SQL.delete_data(f"""UPDATE {self.__table_name} SET
                        deleted_status='{DeletedStatuses.PERMANENTLY_DELETED.value}'
                        WHERE id = {self_id} AND user_id={user_id}""")
        SQL.delete_data(f"""UPDATE '{self.__table_transaction}' SET
                        deleted_status='{DeletedStatuses.CASCADE_DELETED.value}'
                        WHERE category_id = {self_id} AND user_id={user_id}""")
