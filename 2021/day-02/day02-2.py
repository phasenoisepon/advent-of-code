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
        self.aim = 0

    def process_command(self, direction: Directions, distance: int):
        if direction == Directions.forward:
            self.horizontal = self.horizontal + distance
            self.depth = self.depth + self.aim * distance
        elif direction == Directions.down:
            self.aim = self.aim + distance
        elif direction == Directions.up:
            self.aim = self.aim - distance
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
    assert SampleSubmarine.get_result() == 900

    ProductionSubmarine = Command()
    ProductionSubmarine.run_tape(lines_into_tuple_list(file_into_lines("day2.txt")))
    print(f"{ProductionSubmarine=}, {ProductionSubmarine.get_result()=}")

if __name__ == "__main__":
    main()

"""
--- Part Two ---
Based on your calculations, the planned course doesn't seem to make any sense. You find the submarine manual and discover that the process is actually slightly more complicated.

In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. The commands also mean something entirely different than you first thought:

down X increases your aim by X units.
up X decreases your aim by X units.
forward X does two things:
It increases your horizontal position by X units.
It increases your depth by your aim multiplied by X.
Again note that since you're on a submarine, down and up do the opposite of what you might expect: "down" means aiming in the positive direction.

Now, the above example does something different:

forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your depth does not change.
down 5 adds 5 to your aim, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your depth increases by 8*5=40.
up 3 decreases your aim by 3, resulting in a value of 2.
down 8 adds 8 to your aim, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10, your depth increases by 2*10=20 to a total of 60.
After following these new instructions, you would have a horizontal position of 15 and a depth of 60. (Multiplying these produces 900.)

Using this new interpretation of the commands, calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
"""
