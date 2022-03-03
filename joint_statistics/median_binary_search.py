#!/usr/bin/env python3


# find median with binary search from two sorted arrays -- O(log(m+n))
def median_binary_search_from_sorted_arrays(list1, list2) -> float:
    m, n = len(list1), len(list2)
    len_total = m + n
    if len_total % 2 == 1:
        k = (len_total + 1) // 2
        find_two = False
    else:
        k = len_total // 2
        find_two = True

    index1, index2 = 0, 0
    while True:
        # 边界情况
        if index1 == m:
            if find_two:
                return (list2[index2 + k - 1] + list2[index2 + k]) / 2
            else:
                return list2[index2 + k - 1]
        elif index2 == n:
            if find_two:
                return (list1[index1 + k - 1] + list1[index1 + k]) / 2
            else:
                return list1[index1 + k - 1]
        # 正常情况最后一步
        elif k == 1:
            if list1[index1] <= list2[index2]:
                first = list1[index1]
                if not find_two:
                    return first
                if index1 + 1 <= m - 1:
                    second = min(list1[index1 + 1], list2[index2])
                else:
                    second = min(list2[index2], list2[index2 + 1])
                return (first + second) / 2
            else:
                first = list2[index2]
                if not find_two:
                    return first
                if index2 + 1 <= n - 1:
                    second = min(list1[index1], list2[index2 + 1])
                else:
                    second = min(list1[index1], list1[index1 + 1])
                return (first + second) / 2

        # 正常迭代
        pivot_index1 = min(index1 + k // 2 - 1, m - 1)
        pivot_index2 = min(index2 + k // 2 - 1, n - 1)
        pivot1, pivot2 = list1[pivot_index1], list2[pivot_index2]
        if pivot1 <= pivot2:
            k -= pivot_index1 - index1 + 1
            index1 = pivot_index1 + 1
        else:
            k -= pivot_index2 - index2 + 1
            index2 = pivot_index2 + 1


list1 = [1, 2, 4, 5, 8, 9]
list2 = [1, 2, 3]
median = median_binary_search_from_sorted_arrays(list1, list2)
print("median: " + str(median))
