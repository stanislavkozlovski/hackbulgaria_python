import sys


def lexer(polynomial: str):
    derivative = ''
    if len(polynomial) == 1:
        if polynomial.isnumeric():
            # is a constant
            derivative = DerivativeGetter.get_constant_derivative(polynomial)
        else:
            # is a variable. ex: x
            derivative = DerivativeGetter.get_variable_derivative(polynomial)

    elif '^' in polynomial and not polynomial[0].isnumeric():
        # x^4 for example
        derivative = DerivativeGetter.get_variable_power_derivative(polynomial)
    elif '^' in polynomial and polynomial[0].isnumeric():
        # 3x^4 for example
        derivative = DerivativeGetter.get_general_derivative(polynomial)
    else:
        raise Exception("I DONT KNOW WHAT {} IS".format(polynomial))

    return derivative


class DerivativeGetter():
    @staticmethod
    def get_constant_derivative(constant: str):
        # the derivative of a constant is always 0
       # print('The derivative of {} is {}'.format(constant, 0))
        return '0'

    @staticmethod
    def get_variable_derivative(variable: str):
        # the derivative of a variable is always 1
        #print('The derivative of {} is {}'.format(variable, 1))
        return '1'

    @staticmethod
    def get_variable_power_derivative(function: str):
        # the derivative of x^4 is 4*x^(4-1) => 4x^3
        power = int(function[list(function).index('^') + 1:])
        if power == 1:
            # x^1 = 1 * x^0 = 1*1 = 1
            return '1'
        else:
            new_power = power - 1
            if new_power == 1:
                # x^2 => 2 * x^1 => 2x, no power
                new_power = ''
            else:
                # x^3 => 3 * x^2 => 3x^2
                new_power = '^' + str(new_power)

            return str(power) + 'x' + new_power

    @staticmethod
    def get_general_derivative(function: str):
        """
        4x^3 => 4 * 3 * x^(3-1)
        """

        # get the first num, 4 in the above example
        first_num = ''
        var_index = 0  # the index of the variable

        for idx, digit in enumerate(function):
            if digit.isnumeric():
                first_num += digit
            else:
                var_index = idx
                break
        first_num = int(first_num)

        variable = function[var_index]
        # var_index + 1 = ^
        # we get the power, which is var_index+2 till the end of the string
        power = int(str(function[var_index + 2:]))

        # start of calculations

        new_power = power - 1
        if new_power == 1:
            new_power = ''  # x^1 => x
        else:
            new_power = '^' + str(new_power)

        return str(first_num * power) + variable + new_power


def main(input: str):
    import re
    print('The derivative of f(x) = ' + input + ' is:')
    # split the polynomial in parts
    operators = list(filter(lambda x: x != '', re.split(r'[^+-]', input)))
    split_poly = re.split(r'[+ -]', input)

    # get the derivative for each part
    solution = []
    for part in split_poly:
        solution_part = lexer(part)

        if solution_part != '0':
            solution.append(solution_part)

    if not solution:  # == 0
        print("f'(x) = " + str(0))
        exit()

    # try addition in cases like 2x + 4x
    addition = []
    var = ''
    for part in solution:
        import re
        if re.match(r'\d+\w$', part):
            addition.append(part)
            var = part[-1]

    if len(addition) > 1:
        sum = 0
        for part in addition:
            part_num = ''
            for digit in part:
                if digit.isnumeric():
                    part_num += digit
            part_num = int(part_num)
            sum += part_num
        print("f'(x) = " + str(sum) + var)
    else:
        operator_index = 0
        solution_str = ''
        for idx, part in enumerate(solution):
            solution_str += part

            if idx != len(solution) - 1:
                solution_str += ' ' + operators[operator_index] + ' '
                operator_index += 1

        print("f'(x) = " + solution_str)

if __name__ == "__main__":
    #input = sys.argv[1]
    #main(input)  # 4x^3 + 30x^2
    #main('1+x^2')
    main('2x^2+x^2')
    #main('2x^3+x')
    #main('1')
