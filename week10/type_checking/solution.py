import sys
import re

FUNC_DEFINITION_PATTERN = r'(?P<function_name>.+?) :: (?P<input_parameter>.+?) -> (?P<return_parameter>.+?)$'
FUNCTION_NAME_GROUP_KEY = 'function_name'
INPUT_PARAMETER_GROUP_KEY = 'input_parameter'
RETURN_PARAMETER_GROUP_KEY = 'return_parameter'

defined_functions = {
    # key: name of function
    # value: Function object
}


class Function:
    def __init__(self, name, input_parameter, return_parameter):
        self.name = name
        self.input_parameter = input_parameter
        self.return_parameter = return_parameter

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


def eval_definitions(line: str):
    """ Evaluates definitions and returns true if it has
        reached the end of the given definitions"""
    if not line:
        return True
    regex_object = re.search(FUNC_DEFINITION_PATTERN, line)
    function_name = regex_object.group(FUNCTION_NAME_GROUP_KEY)
    input_parameter = regex_object.group(INPUT_PARAMETER_GROUP_KEY)
    return_parameter = regex_object.group(RETURN_PARAMETER_GROUP_KEY)
    defined_functions[function_name] = Function(name=function_name,
                                                input_parameter=input_parameter, return_parameter=return_parameter)

    return False


def eval_composition(line: str):
    functions = line.split(' . ')

    for idx, func_name in enumerate(functions[:-1]):
        function = defined_functions[func_name]
        next_function = defined_functions[functions[idx+1]]
        if next_function.return_parameter != function.input_parameter:
            return False

    return True


def main():
    read_input = [part.rstrip()  # remove the newline at the right
                  for part in list(sys.stdin)]

    for part in read_input:  # loop through the definitions until we reach an empty string
        definitions_have_ended = eval_definitions(part)
        if definitions_have_ended:
            break
    given_composition = read_input[-1]  # the composition is always the last element
    print(eval_composition(given_composition))

if __name__ == '__main__':
    main()