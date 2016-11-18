# arr = [1,2,3,4,5,6,7,8,9,10]
#
# def binary_search(arr, start, end, element):
#     mid = (start+end) // 2
#     mid_el = arr[mid]
#
#     if mid_el == element:
#         return mid
#
#     if mid_el > element:
#         return binary_search(arr, start, mid, element)
#     else:
#         return binary_search(arr, mid, end, element)
#
# print(binary_search(arr, 0, 10, element=9))

"""
Find a point where arrays starts decreasing, array is first increasing and then decreasing.
For example if we have following array [1, 3, 7, 9, 4, 2], the turning point is 4 and index of this point also is 4.

[1, 6, 4, 3, 2] -> Turning point is 4 on index 2.
[1, 4, 5, 2]-> Turning point is 2 on index 3.


"""


def find_turning_point(arr, start, end):
    mid = (start+end) // 2
    mid_el = arr[mid]

    if (mid - 1 >= 0 and mid + 1 < len(arr)
        and arr[mid-1] < mid_el and arr[mid+1] < mid_el):
        return mid  # turning point
    elif mid - 1 < 0 and mid_el > arr[mid+1]:
        return mid  # turning point at start - [4,1,2]
    elif mid + 1 >= len(arr) and mid_el < arr[mid-1]:
        return mid  # turning point at end - [1,4,3]

    if mid-1 >= 0 and mid_el > arr[mid-1]:  # still increasing, so search right
        return find_turning_point(arr, mid, end)

    if mid-1 >= 0 and mid_el < arr[mid-1]: # still decreasing, so search left
        return find_turning_point(arr, start, mid)


test = [1,4,3]
print(find_turning_point(test, 0, len(test)))