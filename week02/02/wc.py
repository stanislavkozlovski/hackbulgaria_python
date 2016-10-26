"""
Implement a Python script, called wc.py that takes two arguments:

A command, that can be one of the following : chars, words, lines
A filename
The script should output, according to the command, the following:

For the command chars, the number of characters in the file
For the command words, the number of words in the file
For the command lines, the number of lines in the file
Examples

Lets have the following text:

story.txt:

Now indulgence dissimilar for his thoroughly has terminated. Agreement offending commanded my an. Change wholly say why eldest period. Are projection put celebrated particular unreserved joy unsatiable its. In then dare good am rose bred or. On am in nearer square wanted.

Of resolve to gravity thought my prepare chamber so. Unsatiable entreaties collecting may sympathize nay interested instrument. If continue building numerous of at relation in margaret. Lasted engage roused mother an am at. Other early while if by do to. Missed living excuse as be. Cause heard fat above first shall for. My smiling to he removal weather on anxious.

Ferrars all spirits his imagine effects amongst neither. It bachelor cheerful of mistaken. Tore has sons put upon wife use bred seen. Its dissimilar invitation ten has discretion unreserved. Had you him humoured jointure ask expenses learning. Blush on in jokes sense do do. Brother hundred he assured reached on up no. On am nearer missed lovers. To it mother extent temper figure better.

Print the chars:

$ python3 wc.py chars story.txt
1032
Print the words:

$ python3 wc.py words story.txt
166
Print the lines:

$ python3 wc.py lines story.txt
6
"""
import sys


def main():
    if len(sys.argv) < 3:
        print("Please input two commands - what you want to count and the file's name")
        print("ex: python3 wc.py words story.txt")
    command = sys.argv[1]
    file_path = sys.argv[2]

    with open(file_path, 'r') as f:
        content = f.readlines()
        if command == "words":
            print(content)
            print(sum([len(words.split()) for words in content]))
        elif command == "lines":
            print(len(content))
        elif command == "chars":
            print(sum([len(word) for words in content for word in words]))


if __name__ == '__main__':
    main()