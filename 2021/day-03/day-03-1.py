from enum import Enum


class Criteria(Enum):
    most_common = "gamma"
    least_common = "epsilon"


def lines_from_file(filename: str) -> list[str]:
    with open(filename) as filehandle:
        return filehandle.readlines()


def n_bit_of_line(line: str, index: int) -> str:
    return line[index]


def bit_list_from_lines(lines: list[str], index: int) -> str:
    return "".join([n_bit_of_line(line, index) for line in lines])


def count_list(bit_list: str, search: str) -> int:
    return bit_list.count(search)


def get_bit_state_from_criteria(bit_list: str, criterion: Criteria) -> str:
    """returns the most or least common bit (as str) in the bit_list"""
    zero = "0"
    zero_count = count_list(bit_list, zero)
    one = "1"
    one_count = count_list(bit_list, one)

    # todo refactor with lists
    if criterion == Criteria.most_common:
        largest = max(zero_count, one_count)
        if largest == zero_count:
            return zero
        elif largest == one_count:
            return one
    elif criterion == Criteria.least_common:
        least = min(zero_count, one_count)
        if least == zero_count:
            return zero
        elif least == one_count:
            return one
    raise Exception("unhandled case")


def criterion_as_bit_string_from_lines(lines: list[str], criterion: Criteria) -> str:
    tmp_list = []
    for i in range(len(lines[0]) - 1):
        tmp_list.append(get_bit_state_from_criteria(bit_list_from_lines(lines, i), criterion))
    return "".join(tmp_list)


def string_as_bits_to_int(string_as_bit: str) -> int:
    return int(string_as_bit, 2)


def power_consumption(epsilon: int, gamma: int) -> int:
    return epsilon * gamma


def power_from_filename(filename: str) -> int:
    lines = lines_from_file(filename)
    gamma_str: str = criterion_as_bit_string_from_lines(lines, Criteria.most_common)
    epsilon_str: str = criterion_as_bit_string_from_lines(lines, Criteria.least_common)
    gamma = string_as_bits_to_int(gamma_str)
    epsilon = string_as_bits_to_int(epsilon_str)
    return power_consumption(epsilon, gamma)


def main():
    sample_lines = lines_from_file("day-03-test.txt")
    sample_bitlist = bit_list_from_lines(sample_lines, 0)
    assert sample_bitlist == "011110011100"
    assert count_list(sample_bitlist, "1") == 7
    assert count_list(sample_bitlist, "0") == 5
    assert get_bit_state_from_criteria(sample_bitlist, Criteria.most_common) == "1"
    assert get_bit_state_from_criteria(sample_bitlist, Criteria.least_common) == "0"
    assert criterion_as_bit_string_from_lines(sample_lines, Criteria.most_common) == "10110"
    assert criterion_as_bit_string_from_lines(sample_lines, Criteria.least_common) == "01001"
    assert string_as_bits_to_int("0") == 0
    assert string_as_bits_to_int("1") == 1
    assert string_as_bits_to_int("101") == 5
    assert string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.least_common)) == 9
    assert string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.most_common)) == 22

    print(
        f"Sample {Criteria.most_common}={string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.most_common))}")
    print(
        f"Sample {Criteria.least_common}={string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.least_common))}")

    sample_epsilon = string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.least_common))
    sample_gamma = string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.most_common))
    assert power_consumption(sample_epsilon, sample_gamma) == 198

    prod_filename = "day-03.txt"
    print(f"{prod_filename=}, power={power_from_filename(prod_filename)}")


if __name__ == "__main__":
    main()

"""
--- Day 3: Binary Diagnostic ---
The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell you many useful things about the conditions of the submarine. The first parameter to check is the power consumption.

You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma rate and the epsilon rate). The power consumption can then be found by multiplying the gamma rate by the epsilon rate.

Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all numbers in the diagnostic report. For example, given the following diagnostic report:

00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1, the first bit of the gamma rate is 1.

The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.

The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and so the final three bits of the gamma rate are 110.

So, the gamma rate is the binary number 10110, or 22 in decimal.

The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)

To begin, get your puzzle input.


"""
