import functools
import operator


def character_score(c):
    if c.islower():
        return ord(c) - ord('a') + 1

    return 26 + ord(c) - ord('A') + 1


def chunk(iter, size):
    print(iter, size)
    return (iter[i:i + size] for i in range(0, len(iter), size))


def per_line(line):
    left, right = line[len(line) // 2:], line[:len(line) // 2]

    return list(set(left) & set(right))[0]


def per_three_lines(lines):
    common = functools.reduce(operator.and_, [set(line.strip()) for line in lines])
    return list(common)[0]


def part1(lines):
    return sum(character_score(per_line(line.strip())) for line in lines)


def part2(lines):
    return sum(character_score(per_three_lines(three_lines)) for three_lines in chunk(lines, 3))


def main():
    with open("input") as f:
        lines = list(f.readlines())

    print("Part 1:  ", part1(lines))
    print("Part 2:  ", part2(lines))


if __name__ == "__main__":
    main()
