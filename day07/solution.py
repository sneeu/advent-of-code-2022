import collections


class Node:
    def __init__(self, name=None, size=None, children=None):
        self.name = name
        self._size = size
        self.children = children

    def __repr__(self):
        return f"Node({self.name}, {self.size}, {self.children})"

    @property
    def size(self):
        return self._size or sum(c.size for c in self.children)

    def walk(self):
        yield self

        if self.children:
            for child in self.children:
                yield from child.walk()



def parse_tree(lines):
    root = Node("", None, [])
    pwd = collections.deque([root])

    for line in lines:
        parts = line.strip().split(" ")

        match parts:
            case ("$", *command):
                match command:
                    case ("cd", "/"):
                        pwd = collections.deque([root])
                    case ("cd", ".."):
                        pwd.pop()
                    case ("cd", name):
                        pwd.append([c for c in pwd[-1].children if c.name == name][0])
                    case ("ls", _):
                        pass
                pass
            case ("dir", name):
                pwd[-1].children.append(Node(name=name, children=[]))
            case (size, name):
                pwd[-1].children.append(Node(name=name, size=int(size)))

    return root


def part1(tree):
    return sum(n.size for n in tree.walk() if n.size < 100000 and n.children)


def part2(tree):
    disk_size = 70000000
    space_used = tree.size
    space_required = 30000000

    space_to_free = (disk_size - space_used - space_required) * -1

    directory_sizes = sorted([n.size for n in tree.walk() if n.children and n.size > space_to_free])

    return directory_sizes[0]


def main():
    with open("input", "r") as f:
        lines = f.readlines()

    root = parse_tree(lines)

    print("Part 1: ", part1(root))
    print("Part 2: ", part2(root))


if __name__ == "__main__":
    main()
