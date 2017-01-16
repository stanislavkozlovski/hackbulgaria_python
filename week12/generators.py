def chain(lst_a, lst_b):
    yield from (lst_a + lst_b)
print(list(chain([1,2], [2,3])))


def compress(iterable, mask):
    yield from (value for idx, value in enumerate(iterable) if mask[idx])

print(list(compress(["Ivo", "Rado", "Panda"], [False, False, True])))


def cycle(iterable):
    while True:
        yield from iterable

endless = cycle(range(0,10))
for item in endless:
    print(item)
