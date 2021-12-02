from enum import Enum


class Directions(Enum):
    forward = "forward"
    down = "down"
    up = "up"


def file_into_lines(filename: str) -> list[str]:
    with open(filename) as filehandle:
        return filehandle.readlines()


def line_into_tuple(line: str) -> tuple[Directions, int]:
    str_split = line.split(' ')
    assert len(str_split) == 2
    assert int(str_split[1]) >= 0
    return Directions[str_split[0]], int(str_split[1])


def lines_into_tuple_list(lines:list[str])->list[tuple[Directions, int]]:
    out_list = []
    for line in lines:
        out_list.append(line_into_tuple(line))
    return out_list


class Command:
    def __init__(self):
        self.horizontal = 0
        self.depth = 0

    def process_command(self, direction: Directions, distance: int):
        if direction == Directions.forward:
            self.horizontal = self.horizontal + distance
        elif direction == Directions.down:
            # reference increasing depth as positive
            self.depth = self.depth + distance
        elif direction == Directions.up:
            self.depth = self.depth - distance
        else:
            raise Exception("unhandled command")

    def get_result(self):
        """
        What do you get if you multiply your final horizontal position by your final depth?
        :return:
        """
        return self.horizontal * self.depth

    def run_tape(self, tape: list[tuple[Directions, int]]) -> None:
        for direction, distance in tape:
            self.process_command(direction, distance)

    def __repr__(self):
        return f"<--Submarine {self.horizontal=}, {self.depth=}-->"

def main():
    assert line_into_tuple("forward 5") == (Directions.forward, 5)
    SampleSubmarine = Command()
    SampleSubmarine.run_tape(lines_into_tuple_list(file_into_lines("sample.txt")))
    assert SampleSubmarine.get_result() == 150

    ProductionSubmarine = Command()
    ProductionSubmarine.run_tape(lines_into_tuple_list(file_into_lines("day2.txt")))
    print(f"{ProductionSubmarine=}, {ProductionSubmarine.get_result()=}")

if __name__ == "__main__":
    main()

"""
--- Day 2: Dive! ---
Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

forward X increases the horizontal position by X units.
down X increases the depth by X units.
up X decreases the depth by X units.
Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result of what you might expect.

The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2
Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

forward 5 adds 5 to your horizontal position, a total of 5.
down 5 adds 5 to your depth, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13.
up 3 decreases your depth by 3, resulting in a value of 2.
down 8 adds 8 to your depth, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15.
After following these instructions, you would have a horizontal position of 15 and a depth of 10. (Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?

To begin, get your puzzle input.
"""
