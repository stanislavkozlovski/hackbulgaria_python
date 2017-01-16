import random


def generate_random_letter():
    should_be_capital = bool(random.randint(0, 1))

    if should_be_capital:
        return chr(random.randint(65, 90))
    else:
        return chr(random.randint(97, 122))

print('Lets make a book!')
print('Please give me: ')

chapter_count = int(input('>Your desired chapter count '))
chapter_length = int(input('>Your desired chapter length '))

book = open('book.txt', 'w')
for i in range(chapter_count):
    left_chapter_length = chapter_length
    book.write(f'Chapter #{i+1}\n')
    while left_chapter_length > 0:
        to_print_new_line = not bool(random.randint(0, 150))
        word_length = random.randint(2, max(2, min(12, left_chapter_length)))
        left_chapter_length -= word_length + 1

        word = ''.join(generate_random_letter() for _ in range(word_length))
        book.write(word + ' ')
        if to_print_new_line:
            book.write('\n')

    book.write('\n\n')
