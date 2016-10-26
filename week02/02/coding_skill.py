"""
The problem where you analyze the given json with data and returns some results.

You have a data.json file in this repo. It is full with people objects. Every person have skills array with languages objects in it. Every skill has name and level.

Write a program that does two things:

Read data.json file as an argument in the console.
Prints all languages and the best person in every language.
$ python3 coding_skill.py data.json
C++ - Cherna Nina
PHP - Rado Rado
Python - Ivo Ivo
C# - Pavli Pavli
Haskell - Rado Rado
Java - Rado Rado
JavaScript - Magi Magi
Ruby - Magi Magi
CSS - Pavli Pavli
C - Cherna Nina
"""
import json
import sys


def main():
    if len(sys.argv) < 2:
        print("Please enter the .json file you want to read from!")
        exit()
    languages = {}
    json_path = sys.argv[1]
    print(json_path)
    # read json
    with open(json_path, 'r', encoding='UTF-8') as json_obj:
        coding_skills = json.load(json_obj)
        people = coding_skills['people']
        languages = get_languages_dict(people)

    for language, people in languages.items():
        most_skilled_person = max(people, key=lambda x: x['level'])['name']
        print("{lang} - {person}".format(lang=language, person=most_skilled_person))


def get_languages_dict(people: dict) -> dict:
    """
    Invert a dictionary of people with certain skillsets of languages to a
    dictionary that holds as key a language and as value a list of names of people and their levels at it
    return ex:
    {'Python': [{'level': 80, 'name': 'IvoIvo'},
            {'level': 66, 'name': 'MagiMagi'},
            {'level': 77, 'name': 'PavliPavli'}
            ],
     'Ruby': [{'level': 35, 'name': 'MagiMagi'}]} }

    """
    languages = {}

    for person in people:
        person_skills = person['skills']
        for skill in person_skills:
            level = skill['level']
            skill_name = skill['name']
            if skill_name not in languages:
                languages[skill_name] = []
            person_level = {'name': person['first_name'] + person['last_name'],
                            'level': level}
            languages[skill_name].append(person_level)

    return languages

if __name__ == '__main__':
    main()