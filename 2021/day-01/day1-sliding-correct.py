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

def sum_list_return_sums(input_list: list[list[int]])->list[list]:
    """sums each sublist and then appends to a side-list"""
    out_list = []
    for sublist in input_list:
        out_list.append([sublist, sum(sublist)])
    return out_list


def read_list_find_asc(input_list)->int:
    previous_sum = None
    counter = 0
    for subl in input_list:
        if previous_sum is None:
            print(f"{subl}: N/A")
        else:
            if subl[1] > previous_sum:
                print(f"{subl}: ascending")
                counter = counter + 1
            elif subl[1] < previous_sum:
                print(f"{subl}: descending")
            else:
                print(f"{subl}: no change")
        previous_sum = subl[1]
    return counter



def main():
    filename = "sample-data.txt"
    sample_int_list = read_file_return_int_list(filename)
    sample_split = split_int_list_into_windows(sample_int_list)
    sample_sum = sum_list_return_sums(sample_split)
    sample_result = read_list_find_asc(sample_sum)
    print(f"{filename=} {sample_result=}")

    print("-------"+"\n"*3)

    filename = "day1.txt"
    int_list = read_file_return_int_list(filename)
    split = split_int_list_into_windows(int_list)
    list_sum = sum_list_return_sums(split)
    result = read_list_find_asc(list_sum)
    print(f"{filename=} {result=}")



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
