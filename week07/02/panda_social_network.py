import re
import json

class InvalidEmailError(Exception):
    pass
class PandaAlreadyThereError(Exception):
    pass
class PandasAlreadyFriendsError(Exception):
    pass

class Panda:
    def __init__(self, name: str, email: str, gender: str):
        self.name = name
        if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            raise InvalidEmailError('Invalid Email!')
        self.email = email
        self.gender = gender

    def __str__(self):
        return 'Panda - {}'.format(self.name)

    def __eq__(self, other):
        return (self.email.lower() == other.email.lower()) and (self.name.lower() == other.name.lower()) and (self.gender.lower() == other.gender.lower())

    def __hash__(self):
        return hash(self.email + self.name + self.gender)

    def gender(self):
        return self.gender

    def email(self):
        return self.email

    def name(self):
        return self.name

    def is_male(self):
        return self.gender.lower() == 'male'

    def is_female(self):
        return self.gender.lower() == 'female'

class SocialNetwork:
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
        if panda1 not in self.pandas:
            self.add_panda(panda1)
        if panda2 not in self.pandas:
            self.add_panda(panda2)
        if panda2 in self.relationships[panda1]:
            raise PandasAlreadyFriendsError

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
        connection_level(panda1, panda2) - returns the connection level between panda1 and panda2. If they are friends, the level is 1.
        Otherwise, count the number of friends you need to go through from panda in order to get to panda2.
        If they are not connected at all, return -1! Return False if one of the pandas are not member of the network.
        :param panda1:
        :param panda2:
        :return:
        """
        from collections import deque
        visited = set()
        def BFS(panda, searched_panda):
            nodes = deque()
            nodes.append(panda)
            level = 0
            while nodes:
                panda = nodes.popleft()
                if str(panda) == 'LEVEL UP':
                    level += 1
                    continue
                nodes.append('LEVEL UP')

                for friend in self.relationships[panda]:
                    if friend == searched_panda:
                        return level + 1
                    if friend not in visited:
                        nodes.append(friend)
                        visited.add(friend)

            return level
        connection_level = BFS(panda1, panda2)
        if not connection_level:
            return False
        return connection_level

    def are_connected(self, panda1, panda2):
        return bool(self.connection_level(panda1, panda2))

    def how_many_gender_in_network(self, level, panda, gender):
        """ Find how many pandas with the given gender there are in the Panda's network, LEVEL levels deep"""
        from collections import deque
        visited = set()

        def BFS(panda):
            nodes = deque()
            nodes.append(panda)
            level = 1
            panda_count = 0
            while nodes:
                panda = nodes.popleft()
                if str(panda) == 'LEVEL UP':
                    level += 1
                    continue
                nodes.append('LEVEL UP')

                for friend in self.relationships[panda]:
                    if friend not in visited:
                        nodes.append(friend)
                        visited.add(friend)
                        if friend.gender == gender:
                            panda_count += 1

            return panda_count

        panda_count = BFS(panda)
        return panda_count

    def save(self, file_name):
        # convert the class objects in our relationships dictionary
        pandas = [str(panda.__dict__) for panda in self.pandas]
        relationships = {str(panda.__dict__):[str(p.__dict__) for p in panda2] for panda, panda2 in self.relationships.items()}
        data = {'pandas': pandas, 'relationships': relationships}
        with open(file_name, 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file)

    @staticmethod
    def load(file_name):
        loaded_social_network = SocialNetwork()
        with open(file_name, 'r', encoding='utf-8') as data:
            loaded_data = json.loads(data.readline())
        # we now have a dictionary, but our Panda 'class' dictionaries are strings, so we need to convert those too
        # add each panda to the social network
        for panda in loaded_data['pandas']:
            # the panda is still a string, so we fix the quotes and convert it to a dict
            panda = json.loads(panda.replace("'", '"'))
            loaded_social_network.add_panda(Panda(name=panda['name'], gender=panda['gender'], email=panda['email']))
        # add each relationship to the social network
        for person, friends in loaded_data['relationships'].items():
            """
            :param person: A Panda
            :param friends: A list of Panda objects represented as dictionaries (strings on load),
                            representing the friends of our person
            """
            panda = json.loads(person.replace("'", '"'))
            panda = Panda(name=panda['name'], gender=panda['gender'], email=panda['email'])
            for friend in friends:
                panda_friend = json.loads(friend.replace("'", '"'))
                panda_friend = Panda(name=panda_friend['name'], gender=panda_friend['gender'], email=panda_friend['email'])
                if not loaded_social_network.are_friends(panda, panda_friend):
                    loaded_social_network.make_friends(panda, panda_friend)


        return loaded_social_network


# network = SocialNetwork()
# ivo = Panda("Ivo", "ivo@pandamail.com", "male")
# rado = Panda("Rado", "rado@pandamail.com", "male")
# tony = Panda("Tony", "tony@pandamail.com", "female")
# roza = Panda("Roza", "roza@pandamail.com", "female")
#
# for panda in [ivo, rado, tony]:
#     network.add_panda(panda)
#
# network.make_friends(ivo, rado)
# network.make_friends(rado, tony)
# network.make_friends(tony, roza)
#
# print(network.connection_level(ivo, rado))# == 1 # True
# print(network.connection_level(ivo, tony))# == 2 # Tru
# print(network.connection_level(ivo, roza))# == 3 # Tru
# print(network.how_many_gender_in_network(1, rado, "female")) # True
# print(network.save('bru.json'))
# network.load('bru.json')
