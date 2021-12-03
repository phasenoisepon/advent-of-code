from enum import Enum
import logging


class Criteria(Enum):
    oxygen = "most_common"
    carbon_dioxide = "least_common"


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
    if criterion == Criteria.oxygen:
        # If 0 and 1 are equally common, keep values with a 1 in the position being considered.
        largest = max(zero_count, one_count)
        if largest == one_count:
            return one
        elif largest == zero_count:
            return zero
    elif criterion == Criteria.carbon_dioxide:
        least = min(zero_count, one_count)
        # If 0 and 1 are equally common, keep values with a 0 in the position being considered.
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

def criterion_search_lines(lines: list[str], criterion: Criteria, depth:int  = 0) -> str:
    if len(lines) == 1:
        return lines[0]
    initial_bitlist = bit_list_from_lines(lines, depth)
    # "most" criterion doesn't mean MOST it means "best fulfills the criterion as per the spec"
    most_criterion = get_bit_state_from_criteria(initial_bitlist, criterion)
    # start eliminating non-most-criterion
    indexes_to_remove = []
    for idx, test_row in enumerate(initial_bitlist):
        if test_row != most_criterion:
            # always keep the higher #'ed idexes at the front
            indexes_to_remove.insert(0, idx)
    curated_lines = lines.copy()
    for index in indexes_to_remove:
        # sanity check
        logging.debug(f"removing {curated_lines[index]} at position {index} since bit {depth} != {most_criterion}")
        assert curated_lines.pop(index) != most_criterion
    return(criterion_search_lines(curated_lines, criterion, depth+1))


def string_as_bits_to_int(string_as_bit: str) -> int:
    return int(string_as_bit, 2)


def power_consumption(epsilon: int, gamma: int) -> int:
    return epsilon * gamma


def power_from_filename(filename: str) -> int:
    lines = lines_from_file(filename)
    gamma_str: str = criterion_as_bit_string_from_lines(lines, Criteria.oxygen)
    epsilon_str: str = criterion_as_bit_string_from_lines(lines, Criteria.carbon_dioxide)
    gamma = string_as_bits_to_int(gamma_str)
    epsilon = string_as_bits_to_int(epsilon_str)
    return power_consumption(epsilon, gamma)


def main():
    logging.basicConfig(level=logging.DEBUG)

    sample_lines = lines_from_file("day-03-test.txt")
    sample_bitlist = bit_list_from_lines(sample_lines, 0)
    assert sample_bitlist == "011110011100"
    assert count_list(sample_bitlist, "1") == 7
    assert count_list(sample_bitlist, "0") == 5
    assert get_bit_state_from_criteria(sample_bitlist, Criteria.oxygen) == "1"
    assert get_bit_state_from_criteria(sample_bitlist, Criteria.carbon_dioxide) == "0"
    assert criterion_as_bit_string_from_lines(sample_lines, Criteria.oxygen) == "10110"
    assert criterion_as_bit_string_from_lines(sample_lines, Criteria.carbon_dioxide) == "01001"
    assert string_as_bits_to_int("0") == 0
    assert string_as_bits_to_int("1") == 1
    assert string_as_bits_to_int("101") == 5
    assert string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.carbon_dioxide)) == 9
    assert string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.oxygen)) == 22

    print(
        f"Sample {Criteria.oxygen}={string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.oxygen))}")
    print(
        f"Sample {Criteria.carbon_dioxide}={string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.carbon_dioxide))}")

    sample_epsilon = string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.carbon_dioxide))
    sample_gamma = string_as_bits_to_int(criterion_as_bit_string_from_lines(sample_lines, Criteria.oxygen))
    assert power_consumption(sample_epsilon, sample_gamma) == 198

    prod_filename = "day-03.txt"
    print(f"{prod_filename=}, power={power_from_filename(prod_filename)}")
    ###
    # part 2
    test_oxygen_str = criterion_search_lines(sample_lines, Criteria.oxygen)
    test_oxygen_int = string_as_bits_to_int(test_oxygen_str)
    print(f"{Criteria.oxygen=}, {test_oxygen_str}, {test_oxygen_int}")
    assert test_oxygen_int == 23

    test_carbon_dioxide_str = criterion_search_lines(sample_lines, Criteria.carbon_dioxide)
    test_carbon_dioxide_int = string_as_bits_to_int(test_carbon_dioxide_str)
    print(f"{Criteria.carbon_dioxide=}, {test_carbon_dioxide_str}, {test_carbon_dioxide_int}")
    assert test_carbon_dioxide_int == 10


    prod_lines = lines_from_file(prod_filename)
    oxygen_int = string_as_bits_to_int(criterion_search_lines(prod_lines, Criteria.oxygen))
    carbon_dioxide_int = string_as_bits_to_int(criterion_search_lines(prod_lines, Criteria.carbon_dioxide))
    print(f"{oxygen_int=}, {carbon_dioxide_int=}, {oxygen_int*carbon_dioxide_int=}")





if __name__ == "__main__":
    main()

"""
--- Part Two ---
Next, you should verify the life support rating, which can be determined by multiplying the oxygen generator rating by the CO2 scrubber rating.

Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in your diagnostic report - finding them is the tricky part. Both values are located using a similar process that involves filtering out values until only one remains. Before searching for either rating value, start with the full list of binary numbers from your diagnostic report and consider just the first bit of those numbers. Then:

Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard numbers which do not match the bit criteria.
If you only have one number left, stop; this is the rating value for which you are searching.
Otherwise, repeat the process, considering the next bit to the right.
The bit criteria depends on which type of rating value you want to find:

To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being considered.
To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the position being considered.
For example, to determine the oxygen generator rating value using the same example diagnostic report from above:

Start with all 12 numbers and consider only the first bit of each number. There are more 1 bits (7) than 0 bits (5), so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000.
In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101.
In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.
In the fifth position, there are an equal number of 0 bits and 1 bits (one each). So, to find the oxygen generator rating, keep the number with a 1 in that position: 10111.
As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.
Then, to determine the CO2 scrubber rating value from the same example above:

Start again with all 12 numbers and consider only the first bit of each number. There are fewer 0 bits (5) than 1 bits (7), so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010.
Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3), so keep only the 2 numbers with a 1 in the second position: 01111 and 01010.
In the third position, there are an equal number of 0 bits and 1 bits (one each). So, to find the CO2 scrubber rating, keep the number with a 0 in that position: 01010.
As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.
Finally, to find the life support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10) to get 230.

Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating, then multiply them together. What is the life support rating of the submarine? (Be sure to represent your answer in decimal, not binary.)


"""
