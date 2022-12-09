import enum
import itertools


class Direction(enum.Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


DIRECTION_VECTOR = {
    Direction.UP: (0, 1),
    Direction.DOWN: (0, -1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
}


class Movement:
    def __init__(self, direction, distance):
        self.direction = direction
        self.distance = distance

    def __repr__(self):
        return f"Movement({self.direction}, {self.distance})"

    @classmethod
    def from_string(cls, s):
        direction, distance = s.split()
        return cls(Direction(direction), int(distance))

    def to_steps(self):
        return itertools.repeat(DIRECTION_VECTOR[self.direction], self.distance)


FOLLOW_VECTORS = {
    (2, 0): (1, 0), # UP
    (2, 2): (1, 1), # UP, RIGHT
    (0, 2): (0, 1), # RIGHT
    (-2, 2): (-1, 1), # DOWN, RIGHT
    (-2, 0): (-1, 0), # DOWN
    (-2, -2): (-1, -1), # DOWN, LEFT
    (0, -2): (0, -1), # LEFT
    (2, -2): (1, -1), # UP, LEFT

    (2, 1): (1, 1),
    (2, -1): (1, -1),
    (-2, 1): (-1, 1),
    (-2, -1): (-1, -1),

    (1, 2): (1, 1),
    (1, -2): (1, -1),
    (-1, 2): (-1, 1),
    (-1, -2): (-1, -1),
}


def parallel_subtract(a, b):
    """
    >>> parallel_subtract((4, 2), (0, 0))
    (4, 2)
    >>> parallel_subtract((4, 2), (2, 3))
    (2, -1)
    >>> parallel_subtract((3, 2), (-5, 1))
    (8, 1)
    """
    return (a[0] - b[0], a[1] - b[1])


def parallel_add(a, b):
    """
    >>> parallel_add((4, 2), (0, 0))
    (4, 2)
    >>> parallel_add((4, 2), (2, 3))
    (6, 5)
    >>> parallel_add((3, 2), (-5, 1))
    (-2, 3)
    """
    return (a[0] + b[0], a[1] + b[1])


def follow(head, tail):
    """
    >>> follow((0, 0), (0, 0))
    >>> follow((2, 0), (0, 0))
    (1, 0)
    >>> follow((-2, -2), (0, 0))
    (-1, -1)
    >>> follow((6, -5), (8, -3))
    (7, -4)
    """
    if head == tail:
        return None
    
    if vector := FOLLOW_VECTORS.get(parallel_subtract(head, tail)):
        return parallel_add(tail, vector)


def part1(moves):
    head = (0, 0)
    tails = [(0, 0)]

    for move in moves:
        for step in move.to_steps():
            head = parallel_add(head, step)

            if tail := follow(head, tails[-1]):
                tails.append(tail)

    return len(set(tails))


def part2(moves):
    knots = [(0, 0)] * 10
    tails = []

    for move in moves:
        for step in move.to_steps():
            knots[0] = parallel_add(knots[0], step)
            
            for i in range(1, len(knots)):
                if next_position := follow(knots[i - 1], knots[i]):
                    knots[i] = next_position
                else:
                    # If a knot doesn't move none of the following will either
                    break

            tails.append(knots[-1])

    return len(set(tails))


def main():
    with open("input") as fh:
        contents = fh.readlines()

    moves = [Movement.from_string(line.strip()) for line in contents]

    print("Part 1: ", part1(moves))
    print("Part 2: ", part2(moves))


if __name__ == "__main__":
    main()
