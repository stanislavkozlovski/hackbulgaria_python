from helpers import convert_to_sql_string, reset_sql
from database import cursor, connection
from exceptions import MissingTableNameError, MissingPrimaryKeyError, MissingColumnError, ExtraColumnsError, InvalidColumns
from fields import IntegerColumn, TextColumn, PrimaryKey, Field


class serializer(type):
    def __new__(mcs, name, bases, clsdict):
        # read the wanted fields
        primary_key = None
        wanted_fields = {}
        for attr, value in clsdict.items():
            if (not callable(value) and not (attr.startswith('__') and attr.endswith('__'))
               and isinstance(value, Field)):
                wanted_fields[attr] = value
                if isinstance(value, PrimaryKey):
                    print('Aaaaaaaa')
                    primary_key = attr
        # remove the fields from the dict
        for attr, _ in wanted_fields.items():
            del clsdict[attr]

        if '_columns' not in clsdict:
            clsdict['_columns'] = {}
        clsdict['_columns'].update(wanted_fields)
        if primary_key is not None:
            clsdict['__primary_key__'] = primary_key
        for base in bases:
            clsdict['_columns'].update(base._columns)
        clsobj = super().__new__(mcs, name, bases, clsdict)
        if not hasattr(clsobj, '__tables__'):
            clsobj.__tables__ = []
        if len(bases) >= 1:
            clsobj.__tables__.append(clsobj)
        # print(clsobj, clsobj.primary_key__)
        return clsobj


class Base(metaclass=serializer):
    """
    Using the 'filter' class, build SQL inside self.select_sql until a get query is called:
        get queries are
            - all()
            - first()
            - get()
    """
    def __init__(self):
        if not hasattr(self, '__tablename__'):
            raise MissingTableNameError('Your table must have a __tablename__ variable set to the name of the table!')
        if not self._contains_primary_key():
            raise MissingPrimaryKeyError('Your table must have exactly one primary key column!')
        self.select_sql = ''

    def __str__(self):
        if self.select_sql:
            return self.select_sql
        return f'{self.__class__.__name__} for the {self.__tablename__}.'

    @classmethod
    def create_tables(cls):
        for table in cls.__tables__:
            table.create_table(table)
        connection.commit()

    def create_table(self):
        """
        CREATE_CLIENTS_TABLE = '''create table if not exists
        clients(id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                salt TEXT,
                email TEXT,
                balance REAL DEFAULT 0,
                message TEXT,
                reset_code TEXT,
                last_blocked TEXT)'''
        :return:
        """
        indent = ' ' * (len(self.__tablename__) + 1)
        columns_str = f',\n{indent}'.join(f'{name} {str(column_type)}' for name, column_type in self._columns.items())
        create_table_sql = f'''CREATE TABLE IF NOT EXISTS
{self.__tablename__}({columns_str})'''

        cursor.execute(create_table_sql)

    def create_obj(self, **kwargs):
        for key in self._columns.keys():
            if isinstance(self._columns[key], PrimaryKey):
                if key in kwargs:
                    raise Exception('You cannot pass a primary key to the table!')
                continue

            if key not in kwargs:
                raise MissingColumnError(f'Your {key} column is missing!')

        if len(kwargs.keys()) >= len(self._columns.keys()):
            raise ExtraColumnsError()
        # save the given obj values
        for key, value in kwargs.items():
            self._columns[key].save_value(value)

        valid_keys = ', '.join(key for key, val in self._columns.items() if not isinstance(val, PrimaryKey))
        valid_values = ', '.join(convert_to_sql_string(val.value) for val in self._columns.values() if not isinstance(val, PrimaryKey))
        insert_sql = f"""INSERT INTO {self.__tablename__}\t({valid_keys}) VALUES ({valid_values});"""

        cursor.execute(insert_sql)
        connection.commit()

    def filter(self, *args, **kwargs):
        """
        Builds an SQL, joining the wanted columns.
        Essentially a WHERE clause.
        Appends each argument with an AND
        :param args: Accepts OrClause objects here
        :param kwargs: Accept keyword arguments, where the key is the column we want and the value is the value we want
        """
        ors = []
        if len(args) != 0:
            for arg in args:
                if not isinstance(arg, OrClause):
                    raise Exception("Expected an OR object!")
                ors.append(arg.sql)  # append the OR sql
                # validate the keys
                for key in arg.keys:
                    if key not in self._columns:
                        raise MissingColumnError(f'Your {key} column is missing!')

        # validate kwags
        for key in kwargs.keys():
            if key not in self._columns:
                raise MissingColumnError(f'Your {key} column is missing!')

        where_annexation = ' AND '.join([' AND '.join(ors),  # all the OR queries
                                         ' AND '.join(f'{name} = {convert_to_sql_string(val)}'  # the traditional kwargs
                                                      for name, val in kwargs.items())])
        if self.select_sql:
            self.select_sql = f'SELECT * FROM ({self.select_sql[:-1]}) WHERE {where_annexation};'
        else:
            self.select_sql = f'SELECT * FROM {self.__tablename__} WHERE {where_annexation};'

        return self

    @reset_sql
    def all(self):
        """
        Gets ALL the documents from the built up query.
        If there is no built up query, we simply return everything
        """
        if not self.select_sql:
            self.select_sql = f'SELECT * FROM {self.__tablename__};'

        documents = cursor.execute(self.select_sql).fetchall()

        # build a dictionary of dictionaries
        all_objects: {int: {}} = {}
        for doc in documents:
            all_objects[doc[self.__primary_key__]] = {key: doc[key] for key in self._columns.keys()}

        return all_objects

    @reset_sql
    def get(self, index):
        """
        Gets ONE document via it's primary key
        :param index:
        :return:
        """
        if self.select_sql:
            self.select_sql = f"SELECT * FROM {(self.select_sql[-1])} WHERE {self.__primary_key__} = {index};"
        else:
            self.select_sql = f"SELECT * FROM {self.__tablename__} WHERE {self.__primary_key__} = {index};"

        result = cursor.execute(self.select_sql).fetchone()

        return {key: result[key] for key in self._columns.keys()}

    @reset_sql
    def first(self):
        if not self.select_sql:
            raise Exception('An all query must follow a filter query')
        result = cursor.execute(self.select_sql).fetchone()

        if result is None:
            raise Exception(f'Nothing found with {self.select_sql}')
        return {key: result[key] for key in self._columns.keys()}

    def _contains_primary_key(self):
        """
        Returns a boolean indicating if we contain a primary key.
        We specifically want only 1 primary key per table
        """
        return len([val for val in self._columns.values() if isinstance(val, PrimaryKey)]) == 1


class OrClause:
    def __init__(self, sql, keys):
        self.sql = sql
        self.keys = keys


def _or(**kwargs) -> OrClause:
    """
    Return a OR query (without a WHERE in front) and the list of the keys
    """
    keys = list(kwargs.keys())

    if len(keys) != 2:
        raise Exception('_or takes exactly 2 keyword arguments!')

    return OrClause(sql=f'({keys[0].lstrip("_")} = {convert_to_sql_string(kwargs[keys[0]])} OR {keys[1].lstrip("_")} = {convert_to_sql_string(kwargs[keys[1]])})',
                    keys=list(key.lstrip('_') for key in keys))


class User(Base):
    __tablename__ = 'users'

    id = PrimaryKey()
    name = TextColumn()
    age = IntegerColumn()


class Student(User):
    __tablename__ = 'students'
    email = TextColumn(10)
    shirt_size = IntegerColumn(3)

Base.create_tables()
user = User()

print(user.filter(_or(name='real', _name='MRO'), age=100).all())
