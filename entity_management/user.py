from typing import Union
from db.tables import user
from db.db import SQL
from utils import DeletedStatuses, TableName
from .abc_entity import EntityABC


class User(EntityABC):
    __table = user
    __table_name = TableName.USER.value
    __table_category = TableName.CATEGORY.value
    __table_transaction = TableName.TRANSACTION.value

    def __init__(self) -> None:
        SQL.create_table(self.__table)

    def create(self, value: tuple) -> Union[None, int]:
        if not SQL.find_one(f"""SELECT login FROM {self.__table_name}
                            WHERE login= '{value[0]}' """):
            return SQL.insert_data(f"""INSERT INTO {self.__table_name}
                                   (login, password) VALUES {value}""")

    def find_one(self, name: str, password: str) -> Union[None, int]:
        user = SQL.find_one(f"""SELECT id FROM {self.__table_name} WHERE
                            login = '{name}' AND password = '{password}' """)
        if user:
            return user['id']

        print('User not found')
        return None

    def get_all(self):
        print(SQL.find_one(f'SELECT * FROM {self.__table_name}'))

    def delete(self, id: int) -> None:
        SQL.delete_data(f"""UPDATE {self.__table_name} SET
                        deleted_status="{DeletedStatuses.PERMANENTLY_DELETED.value}"
                        WHERE id = {id}""")
        SQL.delete_data(f"""UPDATE {self.__table_category} SET
                        deleted_status="{DeletedStatuses.CASCADE_DELETED.value}"
                        WHERE user_id = {id}""")
        SQL.delete_data(f"""UPDATE "{self.__table_transaction}" SET
                        deleted_status="{DeletedStatuses.CASCADE_DELETED.value}"
                        WHERE user_id = {id}""")
