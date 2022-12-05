from collections import deque
import copy


def chunk(iter, size):
    return (iter[i:min(i + size, len(iter))] for i in range(0, len(iter), size))


def apply_operation(state, operation):
    count, source, destination = operation
    for __ in range(0, count):
        state[destination].append(state[source].pop())


def apply_buffered_operation(state, operation):
    count, source, destination = operation

    buffer = deque()

    for __ in range(0, count):
        buffer.append(state[source].pop())

    buffer.reverse()

    state[destination].extend(buffer)


def part1(state, operations):
    for operation in operations:
        apply_operation(state, operation)

    return "".join(stack[-1] for stack in state.values())


def part2(state, operations):
    for operation in operations:
        apply_buffered_operation(state, operation)

    return "".join(stack[-1] for stack in state.values())


def parse_container_string(container_string):
    cleaned = container_string.strip("[] ")

    if len(cleaned) == 0:
        return None

    return cleaned


def parse_file(contents):
    state, operations = [s.split("\n") for s in contents.strip().split("\n\n")]

    stack_rows = list(reversed([[parse_container_string(c) for c in chunk(s, 4)] for s in state[:-1]]))

    stacks = {}

    for stack_row in stack_rows:
        for stack_index, container in enumerate(stack_row):
            if container is not None:
                stacks.setdefault(stack_index + 1, deque())
                stacks[stack_index + 1].append(container)

    parsed_operations = []

    for line in operations:
        operation_, count, from_, source, to_, destination = line.split(" ")

        parsed_operations.append([int(n) for n in (count, source, destination)])

    return stacks, parsed_operations


def main():
    with open("input") as f:
        contents = f.read()

    state, operations = parse_file(contents)

    print("Part 1:  ", part1(copy.deepcopy(state), operations))
    print("Part 2:  ", part2(copy.deepcopy(state), operations))



if __name__ == "__main__":
    main()
