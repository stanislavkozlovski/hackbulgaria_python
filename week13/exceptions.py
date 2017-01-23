class Error(Exception):
    pass


class MissingTableNameError(Error):
    pass


class MissingPrimaryKeyError(Error):
    pass


class MissingColumnError(Error):
    pass


class ExtraColumnsError(Error):
    pass


class InvalidColumns(Error):
    pass