from typing import Union
from db.tables import transaction
from db.db import SQL
from utils import DeletedStatuses, TableName


class Transaction:
    __table = transaction
    __table_name = TableName.TRANSACTION.value
    __table_category = TableName.CATEGORY.value

    def __init__(self) -> None:
        SQL.create_table(self.__table)

    def create(
        self,
        value: int,
        category_id: int,
        user_id: int,
            ) -> Union[None, int]:
        category = SQL.find_one(f"""SELECT id FROM '{self.__table_category}'
                                WHERE id = '{category_id}'
                                AND
                                deleted_status =
                                '{DeletedStatuses.NOT_DELETED.value}'
                                """)
        if category:
            return SQL.insert_data(f"""INSERT INTO '{self.__table_name}'
                    (amount, category_id, user_id)
                    VALUES ({value}, {category_id}, {user_id}) """)

        return None

    def find_one(self, self_id: int, user_id: int) -> None:
        return SQL.find_one(f"""SELECT id, category_id,
                            amount, transaction_date
                                   FROM '{self.__table_name}'
                                   WHERE id = {self_id}
                                   AND user_id = {user_id}
                                   deleted_status =
                                   '{DeletedStatuses.NOT_DELETED.value}'""")

    def get_all(self, user_id: int, parent_id: int = None):
        condition = f"""user_id = {user_id} AND deleted_status =
                                '{DeletedStatuses.NOT_DELETED.value}'"""
        if parent_id:
            condition += f' AND category_id= {parent_id} '
        return SQL.find_many(f"""SELECT id, category_id,
                             amount, transaction_date
                             FROM "{self.__table_name}" WHERE {condition}""")

    def all_expenses(self, user_id: int) -> int:
        amount = SQL.find_one(f"""SELECT SUM(amount) as all_expenses
                      FROM '{self.__table_name}'
                      WHERE user_id = '{user_id}'
                      AND
                      deleted_status =
                      '{DeletedStatuses.NOT_DELETED.value}'
                      """)
        return amount['all_expenses'] if amount['all_expenses'] else 0

    def avg_expenses(self, user_id: int) -> int:
        amount = SQL.find_one(f"""SELECT AVG(amount) as avg_expenses
                      FROM '{self.__table_name}'
                      WHERE user_id = '{user_id}'
                      AND
                      deleted_status =
                      '{DeletedStatuses.NOT_DELETED.value}'
                      """)
        return amount['avg_expenses'] if amount['avg_expenses'] else 0

    def delete(self, self_id: int, user_id: int) -> None:
        SQL.delete_data(f"""UPDATE '{self.__table_name}' SET
                        deleted_status =
                        '{DeletedStatuses.CASCADE_DELETED.value} '
                        WHERE category_id = {self_id} AND user_id={user_id}""")
