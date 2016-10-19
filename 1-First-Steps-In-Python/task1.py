first_name = input("Please enter your name: ")  # type: list
print(first_name)

# for loop
for char in first_name:
    print(char)

list_of_numbers = [5, 3, 8, 9, 2, 6, 1, 44]
for num in list_of_numbers:
    num **= 2

print(list_of_numbers)
# while loop

# If statement
for num in list_of_numbers:
    if num  % 2 == 0:
        print(num)


# create function
def function_1(list_of_even_numbers):
    for num in list_of_even_numbers:
        if num % 2 == 0:
            print(num)

function_1([2,3,4,5,6,7,8])