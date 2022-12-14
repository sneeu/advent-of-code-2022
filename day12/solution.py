import collections


ADJACENT = [(0, 1), (0, -1), (1, 0), (-1, 0)]
PATH_MARKER = {
    (0, 1): "→",
    (0, -1): "←",
    (1, 0): "↓",
    (-1, 0): "↑",
}

class Maze:
    def __init__(self, cells, start, end):
        self.cells = cells
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Maze({self.size()}, start={self.start}, end={self.end})"

    def size(self):
        return len(self.cells), len(self.cells[0])

    def cell(self, x, y):
        w, h = self.size()

        if 0 <= x < w and 0 <= y < h:
            return self.cells[x][y]

    def options(self, x, y):
        height = self.cell(x, y)

        for dx, dy in ADJACENT:
            cell = self.cell(x + dx, y + dy)

            if cell is not None and cell <= height + 1:
                yield (x + dx, y + dy)

    def shortest_path(self, start, end):
        distances = {start: []}
        queue = collections.deque([start])

        while queue:
            current = queue.popleft()
            for option in self.options(*current):
                if option == end:
                    return distances[current] + [option]

                if option in distances:
                    continue

                # We don't need to check lengths because we're doing a
                # breadth-first search, so every distance will be the shortest.
                distances[option] = distances[current] + [option]

                queue.append(option)

        return None

    def from_any_start(self):
        # I have a cold. Please don't judge me.
        w, h = self.size()
        for x in range(w):
            for y in range(h):
                if self.cell(x, y) == 0:
                    shortest = self.shortest_path((x, y), self.end)

                    if shortest:
                        yield shortest

    def print_maze(self, path=None):
        w, h = self.size()

        m = []

        for x in range(w):
            m.append([])
            for y in range(h):
                m[-1].append(chr(self.cells[x][y] + 97))

        if path:
            for i in range(1, len(path)):
                x, y = path[i]
                px, py = path[i - 1]
                
                dx, dy = px - x, py - y
                
                m[x][y] = PATH_MARKER[(dx, dy)]

        for row in m:
            print("".join(row))


def parse_maze(maze_rows):
    maze = []
    start = None
    end = None

    for x, row in enumerate(maze_rows):
        heights = []
        for y, char in enumerate(row.strip()):
            if char == "S":
                start = (x, y)
                height = 0
            elif char == "E":
                end = (x, y)
                height = 25
            else:
                height = ord(char) - ord("a")

            heights.append(height)

        maze.append(heights)

    return Maze(maze, start, end)


def part1(maze):
    path = list(maze.shortest_path(maze.start, maze.end))
    return len(list(path))


def part2(maze):
    return min(len(shortest_path) for shortest_path in maze.from_any_start())


def main():
    with open("input") as f:
        maze_rows = f.readlines()

    maze = parse_maze(maze_rows)

    print("Part 1: ", part1(maze))
    print("Part 2: ", part2(maze))


if __name__ == "__main__":
    main()
