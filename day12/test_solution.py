import pytest

from solution import Maze


@pytest.fixture
def small_maze():
    return Maze([
        [0, 1, 6],
        [3, 2, 5],
        [4, 3, 4],
    ], (0, 0), (0, 2))


def test_maze_size(small_maze):
    assert small_maze.size() == (3, 3)


def test_cell(small_maze):
    assert small_maze.cell(0, 0) == 0
    assert small_maze.cell(0, 1) == 1
    assert small_maze.cell(2, 2) == 4
    assert small_maze.cell(-3, 2) is None


def test_options(small_maze):
    assert list(small_maze.options(0, 0)) == [(0, 1)]
    assert list(small_maze.options(0, 1)) == [(0, 0), (1, 1)]
    assert list(small_maze.options(0, 2)) == [(0, 1), (1, 2)]


def test_shortest_path(small_maze):
    assert list(small_maze.shortest_path(small_maze.start, small_maze.end)) == [
        (0, 1),
        (1, 1),
        (2, 1),
        (2, 2),
        (1, 2),
        (0, 2),
    ]
