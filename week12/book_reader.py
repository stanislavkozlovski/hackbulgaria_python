import os.path


def read_book():
    book_count = 1
    while True:
        book_file_name = str(book_count).zfill(3) + '.txt'

        if not os.path.isfile(book_file_name):
            break

        chapter = []
        with open(book_file_name) as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('# Chapter'):
                    yield ''.join(chapter)
                    chapter = []

                chapter.append(line)

        yield ''.join(chapter) # the last chapter
        book_count += 1


# book_reader = read_book()
for i in read_book():
    print(i)
    command = input()
    while command != ' ':
        command = input()
