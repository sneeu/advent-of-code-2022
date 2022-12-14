import functools
import itertools
import json
import operator


def compare(left, right):
    """
    >>> compare(1, 1)
    >>> compare(1, 2)
    True
    >>> compare(6, 9)
    True
    >>> compare(3, 1)
    False
    >>> compare(8, 7)
    False
    >>> compare([1, 1, 3, 1, 1],  [1, 1, 5, 1, 1])
    True
    >>> compare([], [])
    True
    >>> compare([1], [0])
    False
    >>> compare([1], [1, 2])
    True
    >>> compare([1, 2, 1], [1, 2])
    False
    >>> compare([[1], [2, 3, 4]], [[1], 4])
    True
    >>> compare([9], [[8, 7, 6]])
    False
    >>> compare([[4, 4], 4, 4], [[4, 4], 4, 4, 4])
    True
    >>> compare([7, 7, 7, 7], [7, 7, 7])
    False
    >>> compare([], [3])
    True
    >>> compare([[[]]], [[]])
    False
    >>> compare([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9])
    False
    """

    if type(left) == int and type(right) == int:
        if left < right:
            return True
        elif left > right:
            return False

    if type(left) == list and type(right) == list:
        l = min(len(left), len(right))
        for i in range(l):
            c = compare(left[i], right[i])
            if c is not None:
                return c

        if len(left) < len(right):
            return True
        elif len(left) > len(right):
            return False

        return True

    if type(left) == int and type(right) == list:
        return compare([left], right)
    
    if type(left) == list and type(right) == int:
        return compare(left, [right])


def qsort(seq):
    if len(seq) <= 1:
        return seq

    pivot = seq[0]
    left = [x for x in seq[1:] if compare(x, pivot) == True]
    right = [x for x in seq[1:] if compare(x, pivot) == False]

    return qsort(left) + [pivot] + qsort(right)


def part1(pairs):
    for i, (left, right) in enumerate(pairs):
        if compare(left, right) == True:
            yield i + 1


def part2(pairs):
    dividers = [[[2]], [[6]]]

    packets = qsort(list(itertools.chain(itertools.chain(*pairs), dividers)))

    for i, packet in enumerate(packets):
        if packet in dividers:
            yield (i + 1)


def parse_line(line):
    # Lazy parsing :D
    return json.loads(line)


def main():
    with open("input") as f:
        lines = f.readlines()

    pairs = []

    for i in range(0, len(lines), 3):
        pairs.append((parse_line(lines[i]), parse_line(lines[i + 1])))

    print("Part 1:", sum(part1(pairs)))
    print("Part 2:", functools.reduce(operator.__mul__, part2(pairs)))

if __name__ == "__main__":
    main()
