def convert_to_sql_string(value) -> str:
    """
    Given a value, convert it to a SQL string.
    ex: 3 would stay 3, but a string like AaA would be converted to "AaA"
    """
    if isinstance(value, int):
        return str(value)

    return f'"{str(value)}"'


def reset_sql(func):

    def decorator(*args):
        if len(args) == 0:
            raise Exception('Function should receive a self argument as the first argument!')
        self = args[0]

        results = func(*args)

        self.select_sql = ''
        return results

    return decorator