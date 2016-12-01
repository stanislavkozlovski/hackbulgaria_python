import re
import json
from collections import deque

from custom_exceptions import InvalidEmailError, PandaAlreadyThereError, PandasAlreadyFriendsError


VALID_EMAIL_PATTERN = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


class Panda:
    def __init__(self, name: str, email: str, gender: str):
        if not re.search(VALID_EMAIL_PATTERN, email):
            raise InvalidEmailError('Invalid Email!')
        self.__name = name
        self.__email = email
        self.__gender = gender

    def __str__(self):
        return 'Panda - {}'.format(self.__name)

    def __eq__(self, other):
        return (self.__email.lower() == other.email().lower())\
               and (self.__name.lower() == other.name().lower())\
               and (self.__gender.lower() == other.gender().lower())

    def __hash__(self):
        return hash(self.__email + self.__name + self.__gender)

    def gender(self):
        return self.__gender

    def email(self):
        return self.__email

    def name(self):
        return self.__name

    # unconventional names below but what can you do
    def isMale(self):
        return self.__gender.lower() == 'male'

    def isFemale(self):
        return self.__gender.lower() == 'female'


class PandaSocialNetwork:
    def __init__(self):
        self.pandas = []
        self.relationships = {}

    def add_panda(self, panda: Panda):
        if panda in self.pandas:
            raise PandaAlreadyThereError()

        self.pandas.append(panda)
        self.relationships[panda] = []

    def has_panda(self, panda: Panda):
        return panda in self.pandas

    def make_friends(self, panda1, panda2):
        # see if the pandas are in the social network
        if panda1 not in self.pandas:
            self.add_panda(panda1)
        if panda2 not in self.pandas:
            self.add_panda(panda2)
        if panda2 in self.relationships[panda1]:
            raise PandasAlreadyFriendsError
        # always add a double connection
        self.relationships[panda1].append(panda2)
        self.relationships[panda2].append(panda1)

    def are_friends(self, panda1, panda2):
        return panda1 in self.relationships[panda2]

    def friends_of(self, panda: Panda):
        if panda not in self.relationships.keys():
            return False
        return self.relationships[panda]

    def connection_level(self, panda1, panda2):
        """
        connection_level(panda1, panda2) - returns the connection level between panda1 and panda2.
         If they are friends, the level is 1.
         Otherwise, count the number of friends you need to go through from panda in order to get to panda2.
        If they are not connected at all, return -1! Return False if one of the pandas are not member of the network.
        """
        # check if they're in the social network
        if not self.has_panda(panda1) or not self.has_panda(panda2):
            return -1

        def find_level(panda, searched_panda):
            """
            Use BFS to traverse the graph of relationships, starting from our panda,
            searching for the other panda, tracking at which level we are.
            We add a 'LEVEL UP' placeholder to know when we're going deeper
            """
            visited = {panda}  # keep the nodes we've visited here
            nodes = deque()  # the nodes are pandas
            nodes.extend([panda, 'LEVEL UP'])
            current_level = 0
            while nodes:
                panda = nodes.popleft()
                if str(panda) == 'LEVEL UP':
                    current_level += 1
                    nodes.append('LEVEL UP')
                    if len(nodes) == 1:  # checks if our nodes contain only 'LEVEL UP', in which case we should stop
                        break
                else:
                    # go through the friends of the panda
                    for friend in self.relationships[panda]:
                        if friend == searched_panda:
                            return current_level + 1  # we've found our panda and it's always one level deeper
                        if friend not in visited:
                            nodes.append(friend)
                            visited.add(friend)

        connection_level = find_level(panda1, panda2)
        if not connection_level:
            connection_level = -1  # the friends are not connected

        return connection_level

    def are_connected(self, panda1, panda2):
        # check if two pandas are connected indirectly (friends of friends), using the connection_level function
        return self.connection_level(panda1, panda2) != -1

    def how_many_gender_in_network(self, searched_level, panda, gender):
        """ Find how many pandas with the given gender there are in the Panda's network, LEVEL levels deep"""

        def find_pandas(start_panda):
            """
            Use BFS to traverse the graph of relationships, starting from our panda, searching for the other pandas
            with the given gender up to the certain level, tracking at which level we are.
            We add a 'LEVEL UP' placeholder to know when we're going deeper
            """
            visited = {start_panda}  # type: set
            nodes = deque()  # the nodes are pandas
            nodes.extend([start_panda, 'LEVEL UP'])
            current_level = 1  # 1
            panda_count = 0
            while nodes:
                current_panda = nodes.popleft()
                if str(current_panda) == 'LEVEL UP':
                    current_level += 1
                    nodes.append('LEVEL UP')
                    if len(nodes) == 1:
                        break # checks if our nodes contain only 'LEVEL UP', in which case we should stop
                    elif current_level > searched_level:
                        break  # we've passed the level we're searching in
                else:
                    for friend in self.relationships[current_panda]:
                        if friend not in visited:
                            nodes.append(friend)
                            visited.add(friend)
                            if friend.gender() == gender:
                                panda_count += 1

            return panda_count

        return find_pandas(panda)

    def save(self, file_name):
        """ Save the social network in a json file
        Each Panda class object is converted to a dictionary, holding it's main attributes
        key: pandas
          value: list which holds all the pandas in the social network
        key: relationships
            value: dict - key: holds a Panda
                          value: holds a list of Pandas, friends of the Panda key
        """
        # TODO: You don't need to add each relationship for the social network to be reconstructed
        pandas = [str(panda.__dict__) for panda in self.pandas]
        relationships = {str(panda.__dict__): [str(panda_friend.__dict__) for panda_friend in friends]
                         for panda, friends in self.relationships.items()}
        # save it in the file
        data = {'pandas': pandas, 'relationships': relationships}
        with open(file_name, 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file)

    @staticmethod
    def load(file_name) -> 'PandaSocialNetwork':
        """
        Reconstruct the social network from the contents saved in the .json file
        """
        def __construct_panda(panda_dict: str):
            """ Constructs a panda object from a dictionary that's illustrated in a string"""
            panda = json.loads(panda_dict.replace("'", '"'))
            return Panda(name=panda['_Panda__name'], gender=panda['_Panda__gender'], email=panda['_Panda__email'])

        loaded_social_network = PandaSocialNetwork()
        with open(file_name, 'r', encoding='utf-8') as data:
            loaded_data = json.loads(data.readline())
        # we now have a dictionary, but our Panda 'class' dictionaries are strings, so we need to convert those too

        # add each panda to the social network
        for panda in loaded_data['pandas']:
            # the panda is still a string, so we fix the quotes and convert it to a dict
            loaded_social_network.add_panda(__construct_panda(panda))

        # add each relationship to the social network
        for person, friends in loaded_data['relationships'].items():
            '''
            :param person: A Panda
            :param friends: A list of Panda objects represented as dictionaries (strings on load),
                            representing the friends of our person
            '''
            panda = __construct_panda(person)
            for friend in friends:
                panda_friend = __construct_panda(friend)
                if not loaded_social_network.are_friends(panda, panda_friend):
                    loaded_social_network.make_friends(panda, panda_friend)

        return loaded_social_network

