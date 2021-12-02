n = 3  # n samples


def read_file_return_int_list(filename: str) -> list[int]:
    with open(filename) as file:
        lines = file.readlines()
        return [int(x) for x in lines]


def split_int_list_into_windows(input_list: list[int]):
    assert len(input_list) >= n
    out_list = []
    for idx in range(len(input_list) - n + 1):
        temp_list = []
        for i in range(n):
            temp_list.append(input_list[idx + i])
        assert len(temp_list) == n
        out_list.append(temp_list)
    return out_list


def list_asc_desc(sublist: list[int]) -> int:
    """returns +1 if ascending, 0 if varied, and -1 if descending"""
    ascending = False
    descending = False
    assert len(sublist) == n  # should only be n long sequences
    previous = sublist[0]
    for item in sublist[1:]:
        if item > previous:
            ascending = True
        elif item < previous:
            descending = True
        previous = item

    if ascending and descending:
        return 0
    elif ascending:
        return 1
    elif descending:
        return -1
    else:
        raise Exception("unhandled case")


def assign_delta_windows(input_list: list[list[int]], verbose:bool=False):
    out_windows = []
    for window in input_list:
        if verbose:
            print(f"{window} : {list_asc_desc(window)}")
        out_windows.append([window, list_asc_desc(window)])
    assert len(out_windows) >= 1
    return out_windows


def count_windows(delta_window_list: list[list], criteria: int) -> int:
    """
    :param delta_window_list: window w/ criterion
    :param criteria: int to be used for asc/desc criteria
    :return:  count of windows matching criteria
    """
    counter = 0
    for delta_window in delta_window_list:
        if delta_window[1] == criteria:
            counter = counter + 1
    return counter


def main():
    filename = "sample-data.txt"
    int_list = read_file_return_int_list(filename)
    assert 0 == list_asc_desc([1, 2, 1])
    assert 1 == list_asc_desc([1, 2, 3])
    assert -1 == list_asc_desc([3, 2, 1])
    assert split_int_list_into_windows([1, 2, 3]) == [[1, 2, 3]]
    assert split_int_list_into_windows([1, 2, 3, 4]) == [[1, 2, 3], [2, 3, 4]]
    assert 3 == len(split_int_list_into_windows([1, 2, 3, 4, 5]))
    assert assign_delta_windows(split_int_list_into_windows([1, 2, 3])) == [[[1, 2, 3], 1], ]
    assert assign_delta_windows(split_int_list_into_windows([1, 2, 3, 4])) == [[[1, 2, 3], 1], [[2, 3, 4], 1]]
    assert assign_delta_windows(split_int_list_into_windows([1, 2, 3, 1])) == [[[1, 2, 3], 1], [[2, 3, 1], 0]]
    assert assign_delta_windows(split_int_list_into_windows([1, 2, 1, 0])) == [[[1, 2, 1], 0], [[2, 1, 0], -1]]
    assert count_windows(assign_delta_windows(split_int_list_into_windows([1, 2, 1, 0])), 1) == 0
    assert count_windows(assign_delta_windows(split_int_list_into_windows([1, 2, 1, 0])), -1) == 1

    sign = 1
    sample_split = split_int_list_into_windows(int_list)
    sample_windows = assign_delta_windows(sample_split)
    sample_count = count_windows(sample_windows, sign)
    print(f"{filename=} {sign=} {sample_count=}")
    # get windows
    # find each window asc/desc
    # count asc windows


if __name__ == "__main__":
    main()

"""
--- Part Two ---
Considering every single measurement isn't as useful as you expected: there's just too much noise in the data.

Instead, consider sums of a three-measurement sliding window. Again considering the above example:

199  A
200  A B
208  A B C
210    B C D
200  E   C D
207  E F   D
240  E F G
269    F G H
260      G H
263        H
Start by comparing the first and second three-measurement windows. The measurements in the first window are marked A (199, 200, 208); their sum is 199 + 200 + 208 = 607. The second window is marked B (200, 208, 210); its sum is 618. The sum of measurements in the second window is larger than the sum of the first, so this first comparison increased.

Your goal now is to count the number of times the sum of measurements in this sliding window increases from the previous sum. So, compare A with B, then compare B with C, then C with D, and so on. Stop when there aren't enough measurements left to create a new three-measurement sum.

In the above example, the sum of each three-measurement window is as follows:

A: 607 (N/A - no previous sum)
B: 618 (increased)
C: 618 (no change)
D: 617 (decreased)
E: 647 (increased)
F: 716 (increased)
G: 769 (increased)
H: 792 (increased)
In this example, there are 5 sums that are larger than the previous sum.

Consider sums of a three-measurement sliding window. How many sums are larger than the previous sum?
"""
