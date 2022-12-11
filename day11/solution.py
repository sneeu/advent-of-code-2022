import functools
import operator


class Monkey:
    def __init__(self, monkeys, items, operation, test, true_destination, false_destination):
        self.monkeys = monkeys
        self.items = items
        self.operation = operation
        self.test = test
        self.true_destination = true_destination
        self.false_destination = false_destination

        self.worry_factor = 3
        # In part 2 the numbers get really big, but we can keep them in a
        # "monkey range" by taking the modulo of product of all the tests.
        # That's because we don't really care about the item's worry values,
        # only that it's divisible by the test.

        # Image the tests were 2, 3, and 5. Then an item of worry 66 would have
        # the same behaviour as an item if 66 % (2 * 3 * 5) = 6, that is:
        # * (66 % 30) %2 == 6 % 2
        # * (66 % 30) %3 == 6 % 3
        # * (66 % 30) %5 == 6 % 5
        self.the_monkey_key = None

        self.inspections = 0
        self.items_seen = set()

    def turn(self):
        for item in self.items:
            item = self.operation(item) // self.worry_factor

            self.inspections += 1

            if item % self.test == 0:
                self.monkeys[self.true_destination].send(item)
            else:
                self.monkeys[self.false_destination].send(item)

        self.items = []

    def send(self, item):
        if self.the_monkey_key:
            item = item % self.the_monkey_key

        self.items_seen.add(item)
        self.items.append(item)


def add(x):
    def f(y):
        return x + y

    return f


def mul(x):
    def f(y):
        return x * y

    return f


def squ(x):
    return x ** 2


def part1(monkeys):
    for __ in range(20):
        for monkey in monkeys.values():
            monkey.turn()

    inspections = sorted((monkey.inspections for monkey in monkeys.values()), reverse=True)

    return inspections[0] * inspections[1]


def part2(monkeys):
    the_monkey_key = functools.reduce(operator.__mul__, [m.test for m in monkeys.values()])

    for m in monkeys.values():
        m.worry_factor = 1
        m.the_monkey_key = the_monkey_key

    for __ in range(10_000):
        for monkey in monkeys.values():
            monkey.turn()

    inspections = sorted((monkey.inspections for monkey in monkeys.values()), reverse=True)

    return inspections[0] * inspections[1]


def monkeys():
    m = {}

    m.update({
        0: Monkey(m, [63, 57], mul(11), 7, 6, 2),
        1: Monkey(m, [82, 66, 87, 78, 77, 92, 83], add(1), 11, 5, 0),
        2: Monkey(m, [97, 53, 53, 85, 58, 54], mul(7), 13, 4, 3),
        3: Monkey(m, [50], add(3), 3, 1, 7),
        4: Monkey(m, [64, 69, 52, 65, 73], add(6), 17, 3, 7),
        5: Monkey(m, [57, 91, 65], add(5), 2, 0, 6),
        6: Monkey(m, [67, 91, 84, 78, 60, 69, 99, 83], squ, 5, 2, 4),
        7: Monkey(m, [58, 78, 69, 65], add(7), 19, 5, 1),
    })

    return m


def small_monkeys():
    m = {}

    m.update({
        0: Monkey(m, [79, 98], mul(19), 23, 2, 3),
        1: Monkey(m, [54, 65, 75, 74], add(6), 19, 2, 0),
        2: Monkey(m, [79, 60, 97], squ, 13, 1, 3),
        3: Monkey(m, [74], add(3), 17, 0, 1),
    })

    return m


def main():
    print("Part 1: ", part1(monkeys()))
    print("Part 2: ", part2(monkeys()))


if __name__ == "__main__":
    main()
