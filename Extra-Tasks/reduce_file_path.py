"""
A file path in a Unix OS looks like this - /home/rositsazz/courses/Programming101-Python/week01

We start from the root - / and we navigate to the destination fodler.

But there is a problem - if we have .. and . in our file path, it's not clear where we are going to end up.

.. means to go back one directory
. means to stay in the same directory
we can have more then one / between the directories - /home//code
So for example : /home//rositsazz/courses/./Programming101-Python/week01/../ reduces to /home/rositsazz/courses/Programming101-Python/week01.

Implement a function, called reduce_file_path(path) which takes a string and returns the reduced version of the path.

Every .. means that we have to go one directory back
Every . means that we are staying in the same directory
Every extra / is unnecessary
Always remove the last /
"""


def reduce_file_path(path: str):
    result = []
    folders = path.split('/')  # lists of each folder we want to visit

    for folder in folders:
        if folder == '..' and result != []:
            result.pop()
        elif folder in ['.', '..'] or not folder:
            pass # do nothing
        else:
            result.append(folder)

    if not result:
        return '/'
    return '/' + "/".join(result)

print(reduce_file_path("/"))
# "/"
print(reduce_file_path("/srv/../"))
# "/"
print(reduce_file_path("/srv/www/htdocs/wtf/"))
# "/srv/www/htdocs/wtf"
print(reduce_file_path("/srv/www/htdocs/wtf"))
# "/srv/www/htdocs/wtf"
print(reduce_file_path("/srv/./././././"))
# "/srv"
print(reduce_file_path("/etc//wtf/"))
# "/etc/wtf"
print(reduce_file_path("/etc/../etc/../etc/../"))
# "/"
print(reduce_file_path("//////////////"))
# "/"
print(reduce_file_path("/../"))
# "/"