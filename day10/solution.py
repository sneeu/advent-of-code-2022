def cpu(instructions):
    clock = 0
    state = {
        "x": 1,
    }

    output = {
        clock: state.copy(),
    }

    for instruction in instructions:
        operator, *operand = instruction.split()

        if operator == "addx":
            clock += 1
            output[clock] = state.copy()
            state["x"] += int(operand[0])
            clock += 1
            output[clock] = state.copy()
        if operator == "noop":
            clock += 1
            output[clock] = state.copy()

    return output


def part1(instructions):
    states = cpu(instructions)

    return sum([states[n]["x"] * (n + 1) for n in range(19, 221, 40)])


def part2(instructions):
    states = cpu(instructions)

    for clock, state in states.items():
        x = state["x"]
        if clock % 40 in (x + o for o in [-1, 0, 1]):
            print("#", end="")
        else:
            print(".", end="")
        if (clock + 1) % 40 == 0:
            print()


def main():
    with open("input") as f:
        instructions = f.readlines()

    print("Part 1:", part1(instructions))
    print("Part 2:")
    part2(instructions)


if __name__ == "__main__":
    main()
