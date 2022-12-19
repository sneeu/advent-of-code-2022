import collections
from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def add(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def copy(self):
        return Coord(self.x, self.y)


START = Coord(500, 0)
GRAIN_MOVEMENTS = [
    Coord(-1, 0),
    Coord(-1, -1),
    Coord(-1, 1),
]


def windows(iterable, size):
    """
    >>> list(windows([1, 2, 3, 4, 5], 3))
    [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    >>> list(windows("abcdefg", 2))
    [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('f', 'g')]
    """
    q = collections.deque(maxlen=size)

    for item in iterable:
        q.append(item)
        if len(q) == size:
            yield tuple(q)


def min_max(a, b):
    return min(a, b), max(a, b)


def generate_formation(start, end):
    """
    """
    sx, ex = min_max(start.x, end.x)
    sy, ey = min_max(start.y, end.y)

    if sx != ex:
        for x in range(sx, ex + 1):
            yield Coord(x, sy)
    elif sy != ey:
        for y in range(sy, ey + 1):
            yield Coord(sx, y)


def parse_rocks(lines):
    rocks = set()

    for line in lines:
        forms = []

        for formation in line.split("->"):
            x, y = formation.split(",")

            forms.append(Coord(int(x.strip()), int(y.strip())))

        for start, end in windows(forms, 2):
            rocks.update(generate_formation(start, end))

    return rocks


def bounds(rocks):
    """
    >>> bounds({Coord(1, 3), Coord(2, 1), Coord(3, 2)})
    (Coord(x=1, y=1), Coord(x=3, y=3))
    """
    xs = [rock.x for rock in rocks]
    ys = [rock.y for rock in rocks]

    return Coord(min(xs), min(ys)), Coord(max(xs), max(ys))


def in_bounds(grain, bottom_left, top_right):
    return bottom_left.x <= grain.x <= top_right.x and min(bottom_left.y, 0) <= grain.y <= top_right.y


def print_rocks(rocks, interesting=None):
    if interesting is None:
        interesting = {}

    bottom_left, top_right = bounds(rocks | set(interesting.keys()))

    border = 2

    for y in range(bottom_left.y - border, top_right.y + 1 + border):
        for x in range(bottom_left.x - border, top_right.x + 1 + border):
            c = Coord(x, y)
            if s := interesting.get(c):
                print(s, end="")
            elif c in rocks:
                print("#", end="")
            else:
                print(".", end="")
        print()


def part1(rocks):
    start_rocks = len(rocks)

    bottom_left, top_right = bounds(rocks)

    grain = START.copy()

    while in_bounds(grain, bottom_left, top_right):
        if grain.add(Coord(0, 1)) not in rocks:
            grain = grain.add(Coord(0, 1))
        elif grain.add(Coord(-1, 1)) not in rocks:
            grain = grain.add(Coord(-1, 1))
        elif grain.add(Coord(1, 1)) not in rocks:
            grain = grain.add(Coord(1, 1))
        else:
            rocks.add(grain)
            grain = START.copy()

    return len(rocks) - start_rocks


def add_floor(rocks, floor):
    return rocks | set(generate_formation(Coord(-500, floor), Coord(1500, floor)))


def part2(rocks):
    __, top_right = bounds(rocks)

    floor = top_right.y + 2

    rocks = add_floor(rocks, floor)

    start_rocks = len(rocks)

    grain = START.copy()
    interesting = set()

    while START not in rocks:
        if grain.add(Coord(0, 1)) not in rocks:
            grain = grain.add(Coord(0, 1))
        elif grain.add(Coord(-1, 1)) not in rocks:
            grain = grain.add(Coord(-1, 1))
        elif grain.add(Coord(1, 1)) not in rocks:
            grain = grain.add(Coord(1, 1))
        else:
            rocks.add(grain)
            interesting.add(grain)

            grain = START.copy()

    return len(rocks) - start_rocks


def main():
    with open("input") as fh:
        lines = fh.readlines()

    rocks = parse_rocks(lines)

    print("Part 1: ", part1(rocks.copy()))
    print("Part 2: ", part2(rocks.copy()))


if __name__ == "__main__":
    main()
