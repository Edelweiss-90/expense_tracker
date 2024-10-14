import cmd

from db.db import SQL
from entity_management import Category, Transaction, User
from utils import (access, create_arg_for_transaction, create_arg_for_user,
                   find_by_id, show_graph)

DB_NAME = 'ExpenseTracker.db'
SQL.instance(DB_NAME)


class MyCmd(cmd.Cmd):
    prompt = '>>>'
    __user = User()
    __category = Category()
    __transaction = Transaction()
    _user_id: int

    def check_user_id(self) -> bool:
        return hasattr(self, '_user_id')

    @create_arg_for_user
    def do_login(self, name: str, password: str) -> None:
        id = self.__user.find_one(name, password)
        if id:
            self._user_id = id
            print('Login')

    @create_arg_for_user
    def do_cr_user(self, name: str, password: str) -> None:
        print(name, password, 'Attempt to creating a user...')
        id = self.__user.create((name, password))
        if id:
            self._user_id = id
            print(f'User ID: {id}')
        else:
            print('Login already exists')

    @access
    def do_del_user(self, line) -> None:
        self.__user.delete(self._user_id)
        self._user_id = None
        print('User was deleted')

    @access
    def do_cr_cat(self, line) -> None:
        id = self.__category.create(line, self._user_id)
        if id:
            print(f'Category ID: {id}')

    @access
    def do_all_cat(self, line) -> None:
        categories = self.__category.get_all(self._user_id)

        for category in categories:
            print(f'Category: {category}')

    @access
    @find_by_id
    def do_by_cat(self, id: int) -> None:
        category = self.__category.category_join_tr(id, self._user_id)

        if len(category):
            for tr in category:
                print(f'Transaction: {tr}')
        else:
            print('Transaction: 0')

    @access
    @find_by_id
    def do_graph_by_cat(self, id: int) -> None:
        category = self.__category.category_join_tr(id, self._user_id)

        if len(category):
            transaction_dates: list[str] = []
            transactions: list[int] = []

            for tr in category:
                transactions.append(tr['amount'])
                transaction_dates.append(tr['transaction_date'])

            show_graph(transaction_dates, transactions, 'Transaction Date')
        else:
            print('Transaction: 0')

    @access
    def do_graph_all_cat(self, line) -> None:
        category = self.__category.get_all_ct_with_transaction(self._user_id)

        if len(category):

            listCategory = {}

            for el in category:
                name = el['name']
                amount = el['amount'] if el['amount'] else 0

                listCategory[name] = listCategory.get(name, 0) + amount

            show_graph(
                listCategory.keys(),
                listCategory.values(),
                'Category Name')

        else:
            print('Transaction: 0')

    @access
    @create_arg_for_transaction
    def do_cr_tr(self, price: int, category_id: int) -> None:
        id = self.__transaction.create(price, category_id, self._user_id)
        print(f'Transaction ID: {id}')

    @access
    def do_all_tr(self, line) -> None:
        transactions = self.__transaction.get_all(self._user_id, line)

        for transaction in transactions:
            print(f'Transaction: {transaction}')

    @access
    def do_sum_all_tr(self, line) -> None:
        amount = self.__transaction.all_expenses(self._user_id)
        print(f'All expenses: {amount}')

    @access
    def do_sum_avg_tr(self, line) -> None:
        amount = self.__transaction.avg_expenses(self._user_id)
        print(f'Avg expenses: {amount}')

    @access
    @find_by_id
    def do_find_tr(self, id) -> None:
        transaction = self.__transaction.find_one(id, self._user_id)
        print(f'Transaction: {transaction}')

    def do_exit(self, line) -> bool:
        print('Exit')
        return True


if __name__ == '__main__':
    MyCmd().cmdloop()
