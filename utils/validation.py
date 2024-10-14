def create_arg_for_user(func):
    def wrapper(self, args):
        prepare_args = args.split()
        if len(prepare_args) == 2:
            func(self, prepare_args[0], prepare_args[1])
        else:
            print('Wrong arguments!')
    return wrapper


def create_arg_for_transaction(func):
    def wrapper(self, args):
        prepare_args = args.split()

        if len(prepare_args) == 2 and prepare_args[0].isdigit() and prepare_args[1].isdigit():
            res = tuple(map(to_int, prepare_args))
            func(self, res[0], res[1])
        else:
            print('Wrong arguments!')
    return wrapper


def find_by_id(func):
    def wrapper(self, args):
        if args.isdigit():
            func(self, int(args))
        else:
            print('Wrong arguments!')
    return wrapper


def access(func):
    def wrapper(self, *args):
        if self.check_user_id():
            func(self, *args)
        else:
            print('Permission dance')
    return wrapper


def to_int(arg: str) -> int:
    return int(arg)
